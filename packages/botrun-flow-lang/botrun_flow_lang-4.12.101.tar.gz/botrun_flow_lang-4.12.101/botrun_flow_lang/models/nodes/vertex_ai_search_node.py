import asyncio
import json
from typing import List
import os
import aiohttp
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
import litellm
from google.protobuf.json_format import MessageToDict, MessageToJson

from botrun_flow_lang.models.nodes.llm_node import get_api_key
from botrun_flow_lang.models.nodes.utils import (
    get_search_keywords,
    note_taking_scrape_results,
    scrape_single_url,
)

load_dotenv()

from typing import Any, AsyncGenerator, Dict, List
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
    NodeRunFailedEvent,
    NodeRunStreamEvent,
)
from botrun_flow_lang.models.variable import OutputVariable
from pydantic import Field


class VertexAiSearchNodeData(BaseNodeData):
    """
    @param results: 搜尋結果, 會是一個 List[Dict[str, Any]], dict 長這樣 {"title": "", "url": "", "snippet": ""}
    """

    type: NodeType = NodeType.VERTEX_AI_SEARCH
    search_query: str
    project_id: str
    location: str
    data_store_ids: List[str] = []
    output_variables: List[OutputVariable] = [OutputVariable(variable_name="results")]


class VertexAiSearchNode(BaseNode):
    data: VertexAiSearchNodeData

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在生成搜尋關鍵字...\n",
                is_print=self.data.print_stream,
            )
            keywords = await get_search_keywords(
                self.replace_variables(self.data.search_query, variable_pool)
            )

            for keyword in keywords:
                yield NodeRunStreamEvent(
                    node_id=self.data.id,
                    node_title=self.data.title,
                    node_type=self.data.type.value,
                    chunk=f"- {keyword}\n",
                    is_print=self.data.print_stream,
                )

            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在搜尋關鍵字...\n",
                is_print=self.data.print_stream,
            )
            search_tasks = [self._search_keywords(keyword) for keyword in keywords]
            search_results = await asyncio.gather(*search_tasks)

            selected_urls = await self._choose_related_results(
                self.replace_variables(self.data.search_query, variable_pool),
                search_results,
            )
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在抓取網頁內容...\n",
                is_print=self.data.print_stream,
            )
            scrape_results = await scrape_vertexai_urls(selected_urls, search_results)
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在分析有效內容...\n",
                is_print=self.data.print_stream,
            )

            note_taking_results = await note_taking_scrape_results(
                self.replace_variables(self.data.search_query, variable_pool),
                scrape_results,
            )

            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={
                    "results": note_taking_results,
                },
                is_print=self.data.print_complete,
            )

        except Exception as e:
            import traceback

            traceback.print_exc()
            yield NodeRunFailedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                error=str(e),
                is_print=True,
            )
            raise

    async def _choose_related_results(
        self, user_query: str, items: List[Dict[str, Any]]
    ) -> List[str]:
        """使用 LLM 選擇最相關的搜尋結果"""
        analyze_search_result_prompt = """請分析以下 Google 搜尋結果，參考 snippet 的內容，選出最相關的10個網頁連結，並且彼此內容的重覆性低。
請使用以下幾個優先權來選擇:
1. 如果有政府機關的網站，比如網址包含 gov.tw，請優先選擇政府機關的網站
2. 標題跟使用者問題最相關的
3. 標題包含使用者問題關鍵字的
4. 內容包含使用者問題關鍵字的
5. 網頁連結的內容重覆性低

使用者問題: {question}
搜尋結果: {items}

請務必只使用以下 JSON 格式嚴格回應，不要加上 markdown 格式:
{{
    "urls":["url1", "url2", "url3", "url4", "url5",..."url10"],
}}
"""

        model_name = "openai/gpt-4o-2024-08-06"
        response = litellm.completion(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON.",
                },
                {
                    "role": "user",
                    "content": analyze_search_result_prompt.format(
                        question=user_query,
                        items=json.dumps(items, ensure_ascii=False, indent=2),
                    ),
                },
            ],
            api_key=get_api_key(model_name),
        )

        try:
            selected_urls = json.loads(response.choices[0].message.content)["urls"]
            print(f"selected_urls: {selected_urls}")
            return selected_urls
        except Exception as e:
            print(f"Error parsing LLM response for URL selection: {str(e)}")
            return []

    async def _search_keywords(self, keyword: str) -> List[Dict[str, Any]]:
        """對單個關鍵字進行搜尋"""
        try:
            vertex_search = VertexAISearch()
            all_results = []

            # 對每個 data store 進行平行搜尋
            async def search_data_store(data_store_id: str) -> List[Dict[str, Any]]:
                try:
                    results = vertex_search.vertex_search(
                        project_id=self.data.project_id,
                        location=self.data.location,
                        data_store_id=data_store_id,
                        search_query=keyword,
                    )
                    return results.get("results", [])
                except Exception as e:
                    print(f"Error searching {data_store_id}: {str(e)}")
                    return []

            # 創建所有 data store 的搜尋任務
            search_tasks = [
                search_data_store(data_store_id)
                for data_store_id in self.data.data_store_ids
            ]

            # 平行執行所有搜尋任務
            results_list = await asyncio.gather(*search_tasks)

            # 合併所有結果
            for results in results_list:
                if results:
                    all_results.extend(results)

            return all_results

        except Exception as e:
            print(f"Error in _search_keywords: {str(e)}")
            return []


async def scrape_vertexai_urls(
    selected_urls: List[str], vertexai_search_results: List[Dict]
) -> List[Dict[str, Any]]:
    """並行抓取所有 URL 的內容"""
    scrape_candidates = []
    for keyword_search_result in vertexai_search_results:
        for result in keyword_search_result:
            if result["url"] in selected_urls:
                scrape_candidates.append(result)
    scrape_tasks = []
    for scrape_candidate in scrape_candidates:
        scrape_tasks.append(scrape_single_url(scrape_candidate["url"]))

    # 一次性創建所有 URL 的抓取任務
    scrape_tasks = [scrape_single_url(url) for url in selected_urls]

    # 同時執行所有抓取任務
    scrape_results = await asyncio.gather(*scrape_tasks)
    scrape_results = [
        scrape_result
        for scrape_result in scrape_results
        if scrape_result["status"] == "success"
    ]

    # 轉換為原來的輸出格式
    return scrape_results


class VertexAISearch:
    def __init__(self):
        # 使用與 FirestoreBase 相同的認證方式
        google_service_account_key_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS_FOR_FASTAPI",
            "/app/keys/scoop-386004-d22d99a7afd9.json",
        )
        self.credentials = service_account.Credentials.from_service_account_file(
            google_service_account_key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    def vertex_search(
        self,
        project_id: str,
        location: str,
        data_store_id: str,
        search_query: str,
    ) -> List[discoveryengine.ConverseConversationResponse]:
        try:
            client_options = (
                ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
                if location != "global"
                else None
            )

            client = discoveryengine.SearchServiceClient(
                credentials=self.credentials, client_options=client_options
            )

            serving_config = client.serving_config_path(
                project=project_id,
                location=location,
                data_store=data_store_id,
                serving_config="default_config",
            )

            # 添加 filter 來排除特定檔案類型
            file_filter = 'NOT(mimeType:ANY("application/pdf"))'
            # 建立搜尋請求
            request = discoveryengine.SearchRequest(
                serving_config=serving_config,
                query=search_query,
                # filter=file_filter,
                page_size=10,
            )

            response = client.search(request)

            # 或者使用 JSON 格式（更易讀）
            # print("Response in JSON:")
            # print(MessageToJson(response._pb, indent=2))

            results = []
            for result in response.results:
                # 打印單個結果的詳細信息
                # print("\nSingle Result Details:")
                # print(MessageToJson(result._pb, indent=2))

                document_data = result.document.derived_struct_data
                results.append(
                    {
                        "title": document_data.get("title", "No title"),
                        "url": document_data.get("link", "No link"),
                        "snippet": document_data.get("snippets", "No snippet")[0][
                            "snippet"
                        ],
                        "fileFormat": document_data.get("fileFormat", ""),
                    }
                )

            return {"results": results}

        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"Error occurred: {str(e)}")
            return {"results": []}

    def get_document_content(
        self, project_id: str, location: str, data_store_id: str, document_id: str
    ):
        client = discoveryengine.DocumentServiceClient(credentials=self.credentials)

        name = client.document_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            branch="default_branch",
            document=document_id,
        )

        try:
            document = client.get_document(name=name)
            return document
        except Exception as e:
            print(f"Error getting document: {e}")
            return None


def main():
    # 從環境變數讀取設定
    project_id = "scoop-386004"
    location = "global"
    data_store_ids = [
        "tw-gov-welfare_1730944342934",
        # "tw-gov-welfare-files_1730960173279",
    ]

    # 測試用的搜尋查詢
    search_queries = ["婚前健康檢查", "相關新聞"]
    search_queries = ["苗栗", "生育補助", "相關新聞"]

    # if not all([project_id, data_store_id]):
    #     print("Error: Missing required environment variables.")
    #     print("Please ensure GCP_PROJECT_ID and VERTEX_SEARCH_DATASTORE are set.")
    #     return

    for data_store_id in data_store_ids:
        try:
            vertex_search = VertexAISearch()
            results = vertex_search.vertex_search(
                project_id=project_id,
                location=location,
                data_store_id=data_store_id,
                search_query=" ".join(search_queries),
            )
            print(results)
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
