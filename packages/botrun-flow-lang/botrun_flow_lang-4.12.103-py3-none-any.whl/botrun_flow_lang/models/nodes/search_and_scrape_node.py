from typing import Any, AsyncGenerator, Dict, List
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
    NodeRunFailedEvent,
    NodeRunStreamEvent,
)
import litellm
import json
import aiohttp
import asyncio
from botrun_flow_lang.models.nodes.llm_node import get_api_key
from urllib.parse import quote

from botrun_flow_lang.models.nodes.utils import (
    get_search_keywords,
    note_taking_scrape_results,
    scrape_urls,
)
from botrun_flow_lang.models.variable import OutputVariable
from pydantic import Field
import time


class SearchAndScrapeNodeData(BaseNodeData):
    """
    @param results: 筆記的結果, 會是一個 List[Dict[str, Any]], dict 長這樣{"question": "","url": "","title": "","note": ""}
    """

    type: NodeType = NodeType.SEARCH_AND_SCRAPE
    search_query: str
    output_variables: List[OutputVariable] = [OutputVariable(variable_name="results")]


class SearchAndScrapeNode(BaseNode):
    data: SearchAndScrapeNodeData

    async def _search_question(
        self, question: str, session: aiohttp.ClientSession
    ) -> Dict[str, Any]:
        """執行單個問題的搜尋"""
        url = "https://botrun-flow-lang-fastapi-prod-36186877499.asia-east1.run.app/api/search"
        try:
            async with session.post(
                url,
                json={"query": question, "num": 10},
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "question": question,
                        "status": "success",
                        "items": result["items"],
                    }
                else:
                    return {
                        "question": question,
                        "status": "error",
                        "error": f"Search failed with status {response.status}",
                    }
        except Exception as e:
            return {"question": question, "status": "error", "error": str(e)}

    async def _choose_related_results(
        self, user_query: str, search_results: List[Dict[str, Any]]
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
        items = []
        for result in search_results:
            if result["status"] == "success":
                items.extend(result["items"])

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

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            time_message = []
            time_1 = time.time()
            # 1. 生成搜尋問題
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
            time_2 = time.time()
            time_message.append(f"生成搜尋問題: {time_2 - time_1:.2f} 秒")
            for keyword in keywords:
                yield NodeRunStreamEvent(
                    node_id=self.data.id,
                    node_title=self.data.title,
                    node_type=self.data.type.value,
                    chunk=f"- {keyword}\n",
                    is_print=self.data.print_stream,
                )

            # 2. 執行搜尋
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在將問題交由 Google 搜尋...\n",
                is_print=self.data.print_stream,
            )
            async with aiohttp.ClientSession() as session:
                search_tasks = [
                    self._search_question(question, session) for question in keywords
                ]
                search_results = await asyncio.gather(*search_tasks)
            time_3 = time.time()
            time_message.append(f"將問題交由 Google 搜尋: {time_3 - time_2:.2f} 秒")
            # 使用 asyncio.gather 同步執行所有分析任務
            selected_urls = await self._choose_related_results(
                self.replace_variables(self.data.search_query, variable_pool),
                search_results,
            )
            time_4 = time.time()
            time_message.append(f"選擇相關搜尋結果: {time_4 - time_3:.2f} 秒")
            # print(analyzed_search_results)

            # 3. 抓取網頁內容
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在抓取網頁內容...\n",
                is_print=self.data.print_stream,
            )
            scrape_results = await scrape_urls(selected_urls)
            time_5 = time.time()
            time_message.append(f"抓取網頁內容: {time_5 - time_4:.2f} 秒")
            # 4. 進行筆記
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
            time_6 = time.time()
            time_message.append(f"進行筆記: {time_6 - time_5:.2f} 秒")
            # for result in note_taking_results:
            #     yield NodeRunStreamEvent(
            #         node_id=self.data.id,
            #         node_title=self.data.title,
            #         node_type=self.data.type.value,
            #         chunk=f"完成筆記: {result['question']} ({len(result['note_taking_results'])} 個筆記)\n",
            #         is_print=self.data.print_stream,
            #     )
            for message in time_message:
                print(message)
            # 5. 返回最終結果
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
            yield NodeRunFailedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                error=str(e),
                is_print=True,
            )
            raise
