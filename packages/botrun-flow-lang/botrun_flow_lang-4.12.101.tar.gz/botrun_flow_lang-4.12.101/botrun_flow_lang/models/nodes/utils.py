import asyncio
import json
from typing import Any, Dict, List
from urllib.parse import quote

import aiohttp
import litellm
from yarl import URL

from botrun_flow_lang.models.nodes.llm_node import get_api_key


async def get_search_keywords(search_query: str) -> List[str]:
    """使用 LLM 生成搜尋關鍵字"""
    generate_questions_prompt = """
    你是一個專業的調查員，你會依據以下問題，去網路上搜尋相關資料，並且回答使用者。
    當使用者輸入一個問題時，你會
    1. 理解查詢：理解用戶輸入的查詢。這不僅僅是簡單的關鍵字匹配，而是深入分析查詢的上下文和意圖，以便更準確地理解用戶需求。
    2. 構建查詢：在理解查詢後，你會重構查詢以應其搜索和分析模型。這包括將用戶的自然語言問題轉換為可以在網路上有效搜索的訊息格式，從而提高搜索效率和結果的相關性。
    3. 條列重構查詢：將重構後的查詢，條列成3組搜尋此問題的關鍵字，同一組可以有多個關鍵字，每組關鍵字之間用 空格 隔開。
    4. 每組關鍵字最後面都會加上"相關新聞"。

    以下是使用者輸入的問題:
    {search_query}

    請使用以下 JSON 格式嚴格回應,只包含問題內容,不要使用 markdown 的語法:
    {{
        "keywords":[
            "第1組關鍵字",
            "第2組關鍵字",
            ...
            "最後一組關鍵字"
        ]
    }}
""".format(
        search_query=search_query
    )

    model_name = "anthropic/claude-3-5-sonnet-20241022"
    response = litellm.completion(
        model=model_name,
        messages=[{"role": "user", "content": generate_questions_prompt}],
        api_key=get_api_key(model_name),
    )
    return json.loads(response.choices[0].message.content)["keywords"]


async def scrape_urls(selected_urls: List[str]) -> List[Dict[str, Any]]:
    """並行抓取所有 URL 的內容"""
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


async def scrape_single_url(url: str) -> Dict[str, Any]:
    """抓取單個 URL 的內容"""
    try:
        if "%" not in url:
            quoted_url = quote(url, safe="")
        else:
            quoted_url = url
        scrape_url = f"https://botrun-crawler-fastapi-prod-36186877499.asia-east1.run.app/scrape?url={quoted_url}"
        scrape_url = URL(scrape_url, encoded=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(scrape_url) as response:
                if response.status == 200:
                    body = await response.json()
                    print(f"[scrape_single_url] url: {url}")
                    print(
                        f"[scrape_single_url] content: {body['data']['markdown'][:100]}"
                    )
                    return {
                        "url": url,
                        "title": body["data"]["metadata"]["title"],
                        "content": body["data"]["markdown"],
                        "status": "success",
                    }
                else:
                    return {
                        "url": url,
                        "status": "error",
                        "error": f"Scraping failed with status {response.status}",
                    }
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}


async def note_taking_single_result(
    user_query: str, scrape_result: Dict[str, Any]
) -> Dict[str, Any]:
    """對單個抓取結果進行筆記"""
    note_taker_prompt = """你是一位資料記錄者，並具有基礙程式能力，瞭解 HTML 語法，請分析以下網頁內容，做出詳實記錄。

網頁URL: {url}
網頁標題: {title}
網頁內容: {markdown}

請：
1. 去除不必要的 HTML 資料，
2. 去除與使用者問題無關的行銷內容
3. 去除廣告的內容
4. 去除看起來像是header, footer, sidebar的內容
5. 去除看起來像是版權宣告的內容
6. 去除看起來像是目錄的內容
7. 去除看起來像是導覽列的內容
8. 去除首起來像是連到其它文章的內容

你是記錄者，所以你不要加上任何自己的主觀意見，只做完上述工作後，留下詳實的記錄內容。

請使用以下 JSON 格式嚴格回應，不要附加任何其它文字，不要加上 markdown 的語法:
{{
"url": "網頁URL",
"title": "網頁標題",
"note": "詳實的記錄內容"
}}
"""

    model_name = "gemini/gemini-1.5-flash"
    try:
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
                    "content": note_taker_prompt.format(
                        # user_query=user_query,
                        url=scrape_result["url"],
                        title=scrape_result["title"],
                        markdown=scrape_result["content"],
                    ),
                },
            ],
            api_key=get_api_key(model_name),
        )

        result = json.loads(response.choices[0].message.content)
        print(f"[note_taking_single_result] url: {result['url']}")
        print(f"[note_taking_single_result] title: {result['title']}")
        print(f"[note_taking_single_result] note: {result['note']}")
        return result if result.get("note") else None

    except Exception as e:
        print(f"Error in note taking for URL {scrape_result['url']}: {str(e)}")
        return None


async def note_taking_scrape_results(
    user_query: str, scrape_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """並行處理所有抓取結果的筆記"""
    # 收集所有需要做筆記的任務
    note_tasks = []

    for scrape_result in scrape_results:
        note_tasks.append(note_taking_single_result(user_query, scrape_result))

    # 一次性執行所有筆記任務
    notes = await asyncio.gather(*note_tasks)
    return [note for note in notes if note is not None and note["url"] != ""]
    # 組織結果
