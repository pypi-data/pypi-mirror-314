from copy import deepcopy
from typing import AsyncGenerator
from pydantic import BaseModel
import os
import json
import aiohttp
from dotenv import load_dotenv


load_dotenv()


class PerplexitySearchEvent(BaseModel):
    chunk: str


PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


async def respond_with_perplexity_search(
    input_content, user_prompt_prefix, messages_for_llm, domain_filter: list[str]
) -> AsyncGenerator[PerplexitySearchEvent, None]:
    model = "llama-3.1-sonar-huge-128k-online"
    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        raise ValueError("PPLX_API_KEY environment variable not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # domain_filter = ["*.gov.tw", "-*.gov.cn"]
    payload = {
        "model": model,
        "messages": messages_for_llm,
        "temperature": 0.7,
        "stream": True,
        "search_domain_filter": domain_filter,
    }
    messages = deepcopy(messages_for_llm)
    if user_prompt_prefix:
        messages.append(
            {"role": "user", "parts": [user_prompt_prefix + "\n\n" + input_content]}
        )
    else:
        messages.append({"role": "user", "parts": [input_content]})
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                PERPLEXITY_API_URL, headers=headers, json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Perplexity API error: {error_text}")

                full_response = ""
                async for line in response.content:
                    if line:
                        line = line.decode("utf-8").strip()
                        if line.startswith("data: "):
                            line = line[6:]  # Remove 'data: ' prefix
                            if line == "[DONE]":
                                break

                            try:
                                chunk_data = json.loads(line)
                                # print(chunk_data)
                                if (
                                    chunk_data["choices"][0]
                                    .get("delta", {})
                                    .get("content")
                                ):
                                    content = chunk_data["choices"][0]["delta"][
                                        "content"
                                    ]
                                    full_response += content
                                    yield PerplexitySearchEvent(
                                        chunk=content,
                                    )
                                if chunk_data["choices"][0]["finish_reason"] == "stop":
                                    citations = chunk_data.get("citations", [])
                                    final_citations = []

                                    # 過濾 citations
                                    for citation in citations:
                                        # 檢查是否符合 domain_filter 規則
                                        should_include = False
                                        for filter_rule in domain_filter:
                                            if filter_rule.startswith("-"):
                                                # 排除規則
                                                pattern = filter_rule[1:].replace(
                                                    "*.", ""
                                                )
                                                if pattern in citation:
                                                    should_include = False
                                                    break
                                            else:
                                                # 包含規則
                                                pattern = filter_rule.replace("*.", "")
                                                if pattern in citation:
                                                    should_include = True

                                        if should_include:
                                            final_citations.append(citation)

                                    # 只在有符合條件的 citations 時才產生參考文獻
                                    if final_citations:
                                        references = f"\n\n參考來源：\n"
                                        for citation in final_citations:
                                            references += (
                                                f"- [{citation}]({citation})\n"
                                            )
                                        yield PerplexitySearchEvent(chunk=references)

                            except json.JSONDecodeError:
                                continue

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(e)

    # answer_message = await cl.Message(content="").send()
    # full_response = ""
    # for response in responses:
    #     if response.candidates[0].finish_reason != Candidate.FinishReason.STOP:
    #         # await answer_message.stream_token(response.text)
    #         yield GeminiGroundingEvent(chunk=response.text)
    #         full_response += response.text
    #         if response.candidates[0].grounding_metadata:
    #             if len(response.candidates[0].grounding_metadata.grounding_chunks) > 0:
    #                 references = f"\n\n{tr('Sources:')}\n"
    #                 for grounding_chunk in response.candidates[
    #                     0
    #                 ].grounding_metadata.grounding_chunks:
    #                     references += f"- [{grounding_chunk.web.title}]({grounding_chunk.web.uri})\n"
    #                 # await answer_message.stream_token(references)
    #                 yield GeminiGroundingEvent(chunk=references)
    #     else:
    #         if response.candidates[0].grounding_metadata:
    #             if len(response.candidates[0].grounding_metadata.grounding_chunks) > 0:
    #                 references = f"\n\n{tr('Sources:')}\n"
    #                 for grounding_chunk in response.candidates[
    #                     0
    #                 ].grounding_metadata.grounding_chunks:
    #                     references += f"- [{grounding_chunk.web.title}]({grounding_chunk.web.uri})\n"
    #                 # await answer_message.stream_token(references)
    #                 yield GeminiGroundingEvent(chunk=references)
