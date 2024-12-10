import asyncio
from copy import deepcopy
import sys
import time
from pathlib import Path
from typing import Dict, List
from botrun_flow_lang.models.botrun_app import BotrunApp, BotrunAppMode
from botrun_flow_lang.models.nodes.answer_node import AnswerNodeData
from botrun_flow_lang.models.nodes.base_node import NodeType
from botrun_flow_lang.models.nodes.code_node import CodeNodeData
from botrun_flow_lang.models.nodes.event import (
    NodeRunCompletedEvent,
    NodeRunStartedEvent,
    NodeRunStreamEvent,
    WorkflowRunCompletedEvent,
    WorkflowRunFailedEvent,
)
from botrun_flow_lang.models.nodes.http_request_node import (
    Body,
    BodyType,
    HttpMethod,
    HttpRequestNodeData,
)
from botrun_flow_lang.models.nodes.iteration_node import IterationNodeData
from botrun_flow_lang.models.nodes.perplexity_node import (
    PerplexityModelConfig,
    PerplexityNodeData,
)
from botrun_flow_lang.models.nodes.search_and_scrape_node import (
    SearchAndScrapeNode,
    SearchAndScrapeNodeData,
)
from botrun_flow_lang.models.nodes.vertex_ai_search_node import VertexAiSearchNodeData
from botrun_flow_lang.models.variable import InputVariable, OutputVariable
from botrun_flow_lang.models.workflow import WorkflowData, Workflow
from botrun_flow_lang.models.nodes.start_node import StartNode, StartNodeData
from botrun_flow_lang.models.nodes.llm_node import LLMNodeData, LLMModelConfig
from botrun_flow_lang.models.nodes.end_node import EndNodeData
from botrun_flow_lang.api.workflow.workflow_engine import run_workflow
from botrun_flow_lang.models.workflow_config import WorkflowConfig
from dotenv import load_dotenv
import logging
from datetime import datetime

from botrun_flow_lang.services.user_workflow.user_workflow import UserWorkflow

load_dotenv()


def get_llm_workflow_config():
    botrun_app = BotrunApp(
        name="波文件問",
        description="給波文件問答用的app",
        mode=BotrunAppMode.CHATBOT,
    )

    start_node = StartNodeData(
        title="Start",
    )

    model_config = LLMModelConfig(
        completion_params={
            "max_tokens": 4096,
            "temperature": 0.7,
        },
        mode="chat",
        name="gpt-4o-2024-08-06",
        provider="openai",
    )
    llm_node = LLMNodeData(
        title="LLM",
        model=model_config,
        prompt_template=[
            {
                "role": "system",
                "content": "妳是臺灣人，回答要用臺灣繁體中文正式用語，需要的時候也可以用英文，可以親切、俏皮、幽默，但不能隨便輕浮。在使用者合理的要求下請盡量配合他的需求，不要隨便拒絕",
            },
            {
                "role": "user",
                "content": f"{{{{#{start_node.id}.user_input#}}}}",
            },
        ],
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="user_input")
        ],
        output_variables=[
            OutputVariable(variable_name="llm_output"),
        ],
    )
    answer_node = AnswerNodeData(
        title="Answer",
        input_variables=[
            InputVariable(node_id=llm_node.id, variable_name="llm_output")
        ],
    )
    workflow = WorkflowData(nodes=[start_node, llm_node, answer_node])
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    yaml_str = original_workflow_config.to_yaml()
    return yaml_str


def get_subsidy_workflow_config():
    question_count = 20
    generate_questions_prompt = """
      請以臺灣人的角度,用繁體中文生成 {question_count} 個關於「{subject}」的最常見問題。
  這些問題應該:
  1. 涵蓋不同年齡層父母的疑慮
  2. 包含申請流程、資格條件、金額計算等實際問題
  3. 考慮到不同家庭情況(如單親、低收入戶等)
  4. 包括政策變更、地區差異等相關問題
  5. 涉及實際領取和使用津貼的相關疑問

  請確保問題精確、具體,並且反映臺灣民眾對「{subject}」的真實需求和關切。
  請使用以下 JSON 格式嚴格回應,只包含問題內容:
  [
    {{"問題": "第1個問題內容"}},
    {{"問題": "第2個問題內容"}},
    ...
    {{"問題": "第{question_count}個題內容"}}
    ]
"""

    generate_keywords_prompt = """
  請根據以下關於臺灣育兒津貼政策的問題,生成相關的關鍵字群。每個問題對應一個關鍵字群,關鍵字群應包含3-5個重要的關鍵詞。
  這些關鍵字應該:
  1. 反映問題的核心主題
  2. 包含可能用於搜索相關資訊的詞彙
  3. 涵蓋問題中提到的重要概念或實體

  問題列表:
  {question_list}

  請使用以下 JSON 格式嚴格回應,只包含關鍵字群:
  [
    {{"關鍵字群": ["關鍵字1", "關鍵字2", "關鍵字3"]}},
    {{"關鍵字群": ["關鍵字1", "關鍵字2", "關鍵字3", "關鍵字4"]}},
    ...
  ]
"""
    model_config = LLMModelConfig(
        completion_params={},
        mode="chat",
        name="claude-3-5-sonnet-20241022",
        provider="anthropic",
    )
    botrun_app = BotrunApp(
        name="波津貼", description="有上網功能的 chatbot", mode=BotrunAppMode.CHATBOT
    )

    start_node = StartNodeData(
        title="Start",
    )

    generate_questions_by_llm_node = LLMNodeData(
        title="Generate Questions By LLM",
        model=model_config,
        prompt_template=[
            {
                "role": "user",
                "content": generate_questions_prompt.format(
                    question_count=question_count,
                    subject=f"{{{{#{start_node.id}.user_input#}}}}",
                ),
            },
        ],
        output_variables=[
            OutputVariable(variable_name="llm_output"),
        ],
    )
    get_question_list_from_json_node = CodeNodeData(
        title="Get Question List From JSON",
        code="""
import json
def main(llm_output):
    json_data = json.loads(llm_output)
    question_list = [item["問題"] for item in json_data]
    question_list= "\\n".join(question_list)
    return {"question_list": question_list}

        """,
        input_variables=[
            InputVariable(
                node_id=generate_questions_by_llm_node.id, variable_name="llm_output"
            )
        ],
        output_variables=[
            OutputVariable(variable_name="question_list"),
        ],
    )
    generate_keywords_llm_node = LLMNodeData(
        title="LLM",
        model=model_config,
        prompt_template=[
            {
                "role": "user",
                "content": generate_keywords_prompt.format(
                    question_list=f"{{{{#{get_question_list_from_json_node.id}.question_list#}}}}",
                ),
            },
        ],
        output_variables=[
            OutputVariable(variable_name="llm_output"),
        ],
    )
    get_keyword_list_from_json_node = CodeNodeData(
        title="Get Keyword List From JSON",
        code="""
import json

def main(llm_output):
    json_data = json.loads(llm_output)
    
    all_keywords = []
    for item in json_data:
        all_keywords.append(item["關鍵字群"])
    
    return {"keyword_list": " ".join(all_keywords[0])}
    """,
        input_variables=[
            InputVariable(
                node_id=generate_keywords_llm_node.id, variable_name="llm_output"
            )
        ],
        output_variables=[
            OutputVariable(variable_name="keyword_list"),
        ],
    )
    search_keywords_node = HttpRequestNodeData(
        title="Search Keywords",
        url="https://botrun-flow-lang-fastapi-prod-36186877499.asia-east1.run.app/api/search",
        method=HttpMethod.POST,
        body=Body(
            data={
                "query": f"{{{{#{get_keyword_list_from_json_node.id}.keyword_list#}}}}",
                "num": 3,
            },
            type=BodyType.JSON,
        ),
    )
    get_search_result_from_json_node = CodeNodeData(
        title="Get Search Result From JSON",
        code="""
import json

def main(body, keyword_list):
    search_results = json.loads(body)
    all_search_results = {}
    if "items" in search_results:
        all_search_results[keyword_list] = search_results
    else:
        all_search_results["error"] = "No search results found"

    # 輸出
    formatted_results = json.dumps(all_search_results, ensure_ascii=False, indent=2)
    return {"search_results": formatted_results}

    """,
        input_variables=[
            InputVariable(node_id=search_keywords_node.id, variable_name="body"),
            InputVariable(
                node_id=get_keyword_list_from_json_node.id, variable_name="keyword_list"
            ),
        ],
        output_variables=[
            OutputVariable(variable_name="search_results"),
        ],
    )
    answer_node = AnswerNodeData(
        title="Answer",
        input_variables=[
            InputVariable(
                node_id=generate_keywords_llm_node.id, variable_name="llm_output"
            )
        ],
    )
    workflow = WorkflowData(
        nodes=[
            start_node,
            generate_questions_by_llm_node,
            get_question_list_from_json_node,
            generate_keywords_llm_node,
            get_keyword_list_from_json_node,
            search_keywords_node,
            get_search_result_from_json_node,
            answer_node,
        ]
    )
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    yaml_str = original_workflow_config.to_yaml()
    return yaml_str


def save_yaml_to_file(yaml_str: str, filename: str):
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    file_path = templates_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(yaml_str)
    print(f"YAML 已保存到: {file_path}")


def load_yaml_from_file(filename: str) -> str:
    templates_dir = Path(__file__).parent / "templates"
    file_path = templates_dir / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_perplexity_like_workflow_config():
    is_async = True
    generate_questions_prompt = """
    你是一個專業的調查員，你會依據以下問題，去網路上搜尋相關資料，並且回答使用者。
    當使用者輸入一個問題時，你會
    1. 理解查詢：理解用戶輸入的查詢。這不僅僅是簡單的關鍵字匹配，而是深入分析查詢的上下文和意圖，以便更準確地理解用戶需求。
    2. 重構查詢：在理解查詢後，你會重構查詢以適應其搜索和分析模型。這包括將用戶的自然語言問題轉換為可以在網路上有效搜索的訊息格式，從而提高搜索效率和結果的相關性。
    3. 條列重構查詢：將重構後的查詢，條列成多個子問題，每個子問題都是一個可以在網路上搜尋到的具體問題。

    以下是使用者輸入的問題:
    {question}

    請使用以下 JSON 格式嚴格回應,只包含問題內容:
    [
        "第1個子問題",
        "第2個子問題",
        "最後一個子問題"
    ]
"""
    analyze_search_result_prompt = """請分析以下 Google 搜尋結果，參考 snippet 的內容，選出最相關的三個網頁連結。
問題: {question}
搜尋結果: {search_results}

請使用以下 JSON 格式嚴格回應:
{{
    "selected_urls": ["url1", "url2", "url3"]
}}"""
    note_taker_prompt = """你是一位資料記錄者，請分析以下網頁內容是否與問題相關，並做出詳實記錄。

用來 Google 搜尋的問題: {question}
網頁URL: {url}
網頁標題: {title}
網頁內容: {markdown}

如果內容相關，請提取相關的重要資訊並做詳實記錄。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字:
{{
    "url": "網頁URL",
    "title": "網頁標題",
    "note": "詳實的記錄內容"
}}

如果內容不相關，請回傳空值。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字:
{{
    "url": "",
    "title": "",
    "note": ""
}}
"""
    answer_prompt = """
    你是一個專業的資訊分析員，你會依據以下使用者的問題，以及網路搜尋到的資訊，統整出最完整的回答。
    如果你沒有獲得資訊，請誠實的告訴使用者，不要自行回答。

    {all_info}
    """
    claude_model_config = LLMModelConfig(
        completion_params={},
        name="anthropic/claude-3-5-sonnet-20241022",
    )
    openai_mini_model_config = LLMModelConfig(
        completion_params={},
        name="openai/gpt-4o-mini",
    )
    groq_model_config = LLMModelConfig(
        completion_params={},
        name="groq/llama-3.1-70b-versatile",
    )
    final_model_config = LLMModelConfig(
        completion_params={},
        # name="anthropic/claude-3-5-sonnet-20241022",
        name="gemini/gemini-1.5-pro",
    )
    botrun_app = BotrunApp(
        name="Perplexity Like Search",
        description="有上網搜尋功能的 chatbot",
        mode=BotrunAppMode.CHATBOT,
    )

    start_node = StartNodeData(
        title="Start",
    )
    search_and_scrape_node = SearchAndScrapeNodeData(
        title="Search And Scrape",
        search_query=f"{{{{#{start_node.id}.user_input#}}}}",
        print_stream=True,
    )
    generate_questions_by_llm_node = LLMNodeData(
        title="產生相關議題的問題集...",
        model=openai_mini_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": generate_questions_prompt.format(
                    question=f"{{{{#{start_node.id}.user_input#}}}}",
                ),
            },
        ],
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="history"),
        ],
        print_start=True,
    )
    split_question_list_node = CodeNodeData(
        title="Split Question List",
        code="""
import json
def main(llm_output):
    question_list = json.loads(llm_output)
    return {"question_list": question_list}
        """,
        input_variables=[
            InputVariable(
                node_id=generate_questions_by_llm_node.id, variable_name="llm_output"
            )
        ],
        output_variables=[
            OutputVariable(variable_name="question_list"),
        ],
        # print_complete=True,
    )
    display_doing_research_node = CodeNodeData(
        title="將產生的問題進行 Google 搜尋...",
        code="""
def main():
    return {
        "result": ""
    }
        """,
        input_variables=[],
        output_variables=[],
        print_start=True,
    )
    iteration_question_node = IterationNodeData(
        title="Iteration",
        input_selector=InputVariable(
            node_id=split_question_list_node.id, variable_name="question_list"
        ),
        output_selector=InputVariable(node_id="", variable_name=""),
        is_async=is_async,
    )
    search_question_node = HttpRequestNodeData(
        title="將問題進行 Google 搜尋...",
        url="https://botrun-flow-lang-fastapi-dev-36186877499.asia-east1.run.app/api/search",
        method=HttpMethod.POST,
        body=Body(
            data={
                "query": f"{{{{#{iteration_question_node.id}.item#}}}}",
                "num": 10,
            },
            type=BodyType.JSON,
        ),
    )

    analyze_search_results_node = LLMNodeData(
        title="從搜尋結果中選出最相關的網頁連結...",
        model=openai_mini_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": analyze_search_result_prompt.format(
                    question=f"{{{{#{iteration_question_node.id}.item#}}}}",
                    search_results=f"{{{{#{search_question_node.id}.body#}}}}",
                ),
            },
        ],
        input_variables=[],
        stream=False,
        print_stream=False,
    )

    get_selected_urls_node = CodeNodeData(
        title="取得選定的 URL...",
        code="""
import json
from urllib.parse import quote
def main(llm_output):
    try:
        result = json.loads(llm_output)
        urls = result.get("selected_urls", [])
        if not urls:
            print("No URLs found in LLM output")
            return {"links": []}
            
        final_urls = [quote(url, safe=':/') for url in urls]
        print("Get Selected URLs....")
        print(final_urls)
        return {"links": final_urls}
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM output: {str(e)}")
        return {"links": []}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"links": []}
        """,
        input_variables=[
            InputVariable(
                node_id=analyze_search_results_node.id, variable_name="llm_output"
            ),
        ],
        output_variables=[
            OutputVariable(variable_name="links"),
        ],
        # print_start=True,
        # print_complete=True,
    )

    iteration_scrape_all_pages_node = IterationNodeData(
        title="Iteration Scrape All Pages",
        input_selector=InputVariable(
            node_id=get_selected_urls_node.id, variable_name="links"
        ),
        output_selector=InputVariable(node_id="", variable_name=""),
        is_async=is_async,
    )
    scrape_page_node = HttpRequestNodeData(
        title="Scraping Web Page",
        url="https://botrun-crawler-fastapi-prod-36186877499.asia-east1.run.app/scrape",
        method=HttpMethod.GET,
        params=f"url: {{{{#{iteration_scrape_all_pages_node.id}.item#}}}}",
        # print_start=True,
        # print_complete=True,
    )

    get_scrape_result_markdown_node = CodeNodeData(
        title="將網頁內容轉換成 Markdown 格式...",
        code="""
import json
def main(body, status_code):
    try:
        if status_code == 200:
            body = json.loads(body)
            return {
                "markdown": body["data"]["markdown"],
                "title": body["data"]["metadata"]["title"],
            }
        else:
            return {"markdown": "", "title":""}
    except Exception as e:
        print(f"Error processing [將網頁內容轉換成 Markdown 格式...] result: {str(e)}")
        return {"markdown": "", "title": ""}
        """,
        input_variables=[
            InputVariable(node_id=scrape_page_node.id, variable_name="body"),
            InputVariable(node_id=scrape_page_node.id, variable_name="status_code"),
        ],
        output_variables=[
            OutputVariable(variable_name="markdown"),
            OutputVariable(variable_name="title"),
        ],
        # print_start=True,
    )
    analyze_scrape_result_node = LLMNodeData(
        title="分析網頁內容...",
        model=openai_mini_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": note_taker_prompt.format(
                    question=f"{{{{#{iteration_question_node.id}.item#}}}}",
                    url=f"{{{{#{iteration_scrape_all_pages_node.id}.item#}}}}",
                    title=f"{{{{#{get_scrape_result_markdown_node.id}.title#}}}}",
                    markdown=f"{{{{#{get_scrape_result_markdown_node.id}.markdown#}}}}",
                ),
            },
        ],
        input_variables=[],
        stream=False,
        print_stream=False,
    )
    iteration_scrape_all_pages_node.output_selector = InputVariable(
        node_id=analyze_scrape_result_node.id, variable_name="llm_output"
    )

    combine_all_scrape_results_node = CodeNodeData(
        title="Combine All Scrape Results",
        code="""
import json
def main(item, output):
    results=[]
    for result in output:
        data = json.loads(result)
        if data.get("url") and data.get("title") and data.get("note"):
            data["google_question"] = item
            results.append(data)
    return {"results": results}
        """,
        input_variables=[
            InputVariable(node_id=iteration_question_node.id, variable_name="item"),
            InputVariable(
                node_id=iteration_scrape_all_pages_node.id, variable_name="output"
            ),
        ],
        output_variables=[
            OutputVariable(variable_name="results"),
        ],
        # print_start=True,
        # print_complete=True,
    )
    iteration_question_node.output_selector = InputVariable(
        node_id=combine_all_scrape_results_node.id, variable_name="results"
    )

    consolidate_all_info = CodeNodeData(
        title="Consolidating All Information",
        code="""
import json
def main(user_input, results):
    all_info = f"使用者輸入的問題:\\n{user_input}\\n\\n"
    data = json.dumps(results, ensure_ascii=False, indent=2)
    # print(daa[:200])
    all_info += f"網路搜尋回來的資訊:\\n{data}\\n"
        
    return {"all_info": all_info}
""",
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="user_input"),
            InputVariable(node_id=search_and_scrape_node.id, variable_name="results"),
        ],
        output_variables=[
            OutputVariable(variable_name="all_info"),
        ],
        # print_start=True,
        # print_complete=True,
    )

    answer_llm_node = LLMNodeData(
        title="做完研究後最後的回答...",
        model=claude_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": answer_prompt.format(
                    all_info=f"{{{{#{consolidate_all_info.id}.all_info#}}}}",
                ),
            },
        ],
        input_variables=[InputVariable(node_id=start_node.id, variable_name="history")],
        print_start=True,
    )
    get_reference_links_node = CodeNodeData(
        title="取得參考資料的連結...",
        code="""
import json
def main(results):
    references = []
    for result in results:
        if result.get("note") and result.get("url") and result.get("title"):
            references.append(f"- [{result['title']}]({result['url']})")
    
    if references:
        references=list(set(references))
        text = "參考資料:\\n" + "\\n".join(references)
        return {"result": text}
    return {"result": ""}
""",
        input_variables=[
            InputVariable(node_id=search_and_scrape_node.id, variable_name="results")
        ],
        output_variables=[
            OutputVariable(variable_name="result"),
        ],
        complete_output="result",
    )

    answer_node = AnswerNodeData(
        title="Answer",
        input_variables=[
            InputVariable(node_id=answer_llm_node.id, variable_name="llm_output")
        ],
    )
    workflow = WorkflowData(
        nodes=[
            start_node,
            search_and_scrape_node,
            # generate_questions_by_llm_node,
            # split_question_list_node,
            # display_doing_research_node,
            # [
            #     iteration_question_node,
            #     search_question_node,
            #     analyze_search_results_node,
            #     get_selected_urls_node,
            #     [
            #         iteration_scrape_all_pages_node,
            #         scrape_page_node,
            #         get_scrape_result_markdown_node,
            #         analyze_scrape_result_node,
            #     ],
            #     combine_all_scrape_results_node,
            # ],
            consolidate_all_info,
            answer_llm_node,
            get_reference_links_node,
            answer_node,
        ]
    )
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    return original_workflow_config


def get_perplexity_workflow_config():
    botrun_app = BotrunApp(
        name="Perplexity Search",
        description="使用 perplexity 搜尋的 chatbot",
        mode=BotrunAppMode.CHATBOT,
    )
    start_node = StartNodeData(
        title="Start",
    )
    perplexitly_model_config = PerplexityModelConfig(
        completion_params={},
        name="llama-3.1-sonar-huge-128k-online",
    )

    perplexity_node = PerplexityNodeData(
        title="Perplexity Search",
        model=perplexitly_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": f"""
                幫我根據使用者的提問進行回答，你會尋找最新的資料，而且會以政府網站為優先，最後加上參考資料來源。

                以下是使用者的提問：
                {{{{#{start_node.id}.user_input#}}}}""",
            },
        ],
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="history"),
        ],
    )
    answer_node = AnswerNodeData(
        title="Answer",
        input_variables=[
            InputVariable(node_id=perplexity_node.id, variable_name="perplexity_output")
        ],
    )
    workflow = WorkflowData(
        nodes=[
            start_node,
            perplexity_node,
            answer_node,
        ]
    )
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    return original_workflow_config


def get_vertexai_workflow_config():
    answer_prompt = """
    你是一個專業的資訊分析員，你會依據以下使用者的問題，以及網路搜尋到的資訊，統整出最完整的回答。
    如果你沒有獲得資訊，請誠實的告訴使用者，不要自行回答。

    {all_info}
    """
    claude_model_config = LLMModelConfig(
        completion_params={},
        name="anthropic/claude-3-5-sonnet-20241022",
    )
    gemini_model_config = LLMModelConfig(
        completion_params={},
        name="gemini/gemini-1.5-pro",
    )
    botrun_app = BotrunApp(
        name="Vertex AI Search",
        description="使用 Vertex AI 搜尋的 chatbot",
        mode=BotrunAppMode.CHATBOT,
    )
    start_node = StartNodeData(
        title="Start",
    )

    vertexai_search_node = VertexAiSearchNodeData(
        title="Vertex AI Search",
        search_query=f"{{{{#{start_node.id}.user_input#}}}}",
        project_id="scoop-386004",
        location="global",
        data_store_ids=["tw-gov-welfare_1730944342934"],
        print_stream=True,
    )
    consolidate_all_info = CodeNodeData(
        title="Consolidating All Information",
        code="""
import json
def main(user_input, results):
    all_info = f"使用者輸入的問題:\\n{user_input}\\n\\n"
    data = json.dumps(results, ensure_ascii=False, indent=2)
    # print(daa[:200])
    all_info += f"網路搜尋回來的資訊:\\n{data}\\n"
        
    return {"all_info": all_info}
""",
        input_variables=[
            InputVariable(node_id=start_node.id, variable_name="user_input"),
            InputVariable(node_id=vertexai_search_node.id, variable_name="results"),
        ],
        output_variables=[
            OutputVariable(variable_name="all_info"),
        ],
        # print_start=True,
        # print_complete=True,
    )

    answer_llm_node = LLMNodeData(
        title="做完研究後最後的回答...",
        model=gemini_model_config,
        prompt_template=[
            {
                "role": "user",
                "content": answer_prompt.format(
                    all_info=f"{{{{#{consolidate_all_info.id}.all_info#}}}}",
                ),
            },
        ],
        input_variables=[InputVariable(node_id=start_node.id, variable_name="history")],
        print_start=True,
    )
    get_reference_links_node = CodeNodeData(
        title="取得參考資料的連結...",
        code="""
import json
def main(results):
    references = []
    for result in results:
        if result.get("note") and result.get("url") and result.get("title"):
            references.append(f"- [{result['title']}]({result['url']})")
    
    if references:
        references=list(set(references))
        text = "參考資料:\\n" + "\\n".join(references)
        return {"result": text}
    return {"result": ""}
""",
        input_variables=[
            InputVariable(node_id=vertexai_search_node.id, variable_name="results")
        ],
        output_variables=[
            OutputVariable(variable_name="result"),
        ],
        complete_output="result",
    )

    answer_node = AnswerNodeData(
        title="Answer",
        input_variables=[
            InputVariable(node_id=answer_llm_node.id, variable_name="llm_output")
        ],
    )
    workflow = WorkflowData(
        nodes=[
            start_node,
            vertexai_search_node,
            consolidate_all_info,
            answer_llm_node,
            get_reference_links_node,
            answer_node,
        ]
    )
    original_workflow_config = WorkflowConfig(botrun_app=botrun_app, workflow=workflow)
    return original_workflow_config


async def run_workflow_from_yaml(yaml_str, user_input, history: List[Dict] = []):
    # Setup logger
    log_dir = Path(__file__).parent / "log"
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # log_file = log_dir / f"workflow-{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            # logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)

    logger.info(f"Starting workflow with user input: {user_input}")

    workflow_config = WorkflowConfig.from_yaml(yaml_str)
    workflow = Workflow.from_workflow_data(workflow_config.workflow)

    initial_variable_pool = {}
    # Set StartNode's user_input
    for item in workflow.items:
        if isinstance(item.node, StartNode):
            initial_variable_pool[item.node.data.id] = {}
            for output_variable in item.node.data.output_variables:
                if output_variable.variable_name == "history":
                    initial_variable_pool[item.node.data.id][
                        output_variable.variable_name
                    ] = history
                elif output_variable.variable_name == "user_input":
                    initial_variable_pool[item.node.data.id][
                        output_variable.variable_name
                    ] = user_input
            logger.info(f"Initialized StartNode with input: {user_input}")
            break

    generator = run_workflow(workflow, initial_variable_pool)
    async for event in generator:
        if isinstance(event, NodeRunStartedEvent) and event.is_print:
            # print(f"Node {event.node_title} started <=====")
            logger.info(f"Node {event.node_title} started <=====")
        elif isinstance(event, NodeRunStreamEvent) and event.is_print:
            print(event.chunk, end="", flush=True)
            # logger.info(event.chunk)
        elif isinstance(event, NodeRunCompletedEvent):
            if event.complete_output:
                content = event.outputs.get(event.complete_output, "")
                print(content)
            if event.is_print:
                logger.info(f"{event.outputs}")
        elif isinstance(event, WorkflowRunCompletedEvent):
            exe_times = deepcopy(event.execution_times)
            exe_times.sort(reverse=True)
            for exe_time in exe_times:
                print(exe_time)
            return event.outputs
        elif isinstance(event, WorkflowRunFailedEvent):
            error_msg = f"Workflow failed: {event.error}"
            print(f"\n{error_msg}")
            logger.error(error_msg)
            return None

    return None


if __name__ == "__main__":
    # yaml_str = get_llm_workflow_config()
    # final_output = asyncio.run(
    #     run_workflow_from_yaml(yaml_str, "告訴我一個小紅帽的故事")
    # )
    # exit(0)
    # yaml_str = get_subsidy_workflow_config()
    # yaml_file_name = "subsidy_workflow.yml"
    # workflow_config = get_perplexity_like_workflow_config()
    # yaml_file_name = "perplexity_like_workflow.yml"
    # workflow_config = get_perplexity_workflow_config()
    # yaml_file_name = "perplexity_workflow.yml"
    workflow_config = get_vertexai_workflow_config()
    yaml_file_name = "vertexai_workflow.yml"
    save_yaml_to_file(workflow_config.to_yaml(), yaml_file_name)
    user_workflow = UserWorkflow(
        user_id="sebastian.hsu@gmail.com",
        id="1234abcd",
        workflow_config_yaml=workflow_config.to_yaml(),
    )
    json_str = user_workflow.model_dump_json(indent=2)
    print(json_str)

    # 从文件读取 YAML
    loaded_yaml_str = load_yaml_from_file(yaml_file_name)
    question = "請問新北與高雄市的育兒津貼政策有哪些差異？"
    # question = "請問屏東的長照補助或津貼，與花蓮的差異為何？"
    # question = "我剛生了一對雙胞胎，政府有沒有補助？"
    # question = "中高齡失業，中央以及各縣市有哪些補助？"
    question = "如果寶寶已經滿兩歲了，由衛福部負責0至未滿2歲幼兒的育兒津貼，這個部分就不能再領了嗎？那我需要重新申請教育部負責2至未滿5歲幼兒的育兒津貼嗎？"
    question = "婚前健康檢查補助的費用及檢查項目內容有哪些？新北市跟雲林縣的差異是什麼？幫我做很詳實的比較。"
    # question = "我需要新竹縣所有鄉鎮的生育獎勵補助金額，請全部列出來"
    start_time = time.time()
    final_output = asyncio.run(
        run_workflow_from_yaml(
            loaded_yaml_str,
            question,
        )
    )
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    # if final_output:
    #     print("Workflow completed. Final output:")
    #     print(final_output)
    # else:
    #     print("Workflow did not complete successfully.")
