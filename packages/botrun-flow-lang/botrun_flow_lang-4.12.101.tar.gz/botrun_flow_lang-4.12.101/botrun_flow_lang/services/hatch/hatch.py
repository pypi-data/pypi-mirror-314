from typing import List
from pydantic import BaseModel, Field


class Hatch(BaseModel):
    """
    @user_prompt_prefix: 每次的 user prompt 前面都會加入這段文字
    @search_domain_filter: 搜尋的網域限制, 目前只有針對 perplexit 有效, 範例：["*.gov.tw", "-*.gov.cn"]
    """

    user_id: str
    id: str
    prompt_template: str
    user_prompt_prefix: str = ""
    name: str = ""  # 将 name 设为可选字段，默认为空字符串
    is_default: bool = False
    enable_search: bool = False
    related_question_prompt: str = ""
    search_vendor: str = "perplexity"
    search_domain_filter: List[str] = []
