import os
from dotenv import load_dotenv

load_dotenv()

TAIDE_MODELS = [
    "openai/Llama-3.1-405B-Instruct-FP8",
    "openai/Llama-3.1-70B",
    "openai/Llama-3.1-Nemotron-70B-Instruct",
    "openai/Llama3-TAIDE-LX-70B-Chat",
    "openai/TAIDE-LX-70B-Chat",
]


def get_api_key(model_name: str) -> str:
    if model_name in TAIDE_MODELS or model_name.startswith("taide/"):
        return os.getenv("TAIDE_API_KEY", "")
    elif model_name.startswith("anthropic"):
        return os.getenv("ANTHROPIC_API_KEY", "")
    elif model_name.startswith("openai"):
        return os.getenv("OPENAI_API_KEY", "")
    elif model_name.startswith("gemini"):
        return os.getenv("GEMINI_API_KEY", "")
    elif model_name.startswith("together_ai"):
        return os.getenv("TOGETHERAI_API_KEY", "")
    elif model_name.startswith("deepinfra"):
        return os.getenv("DEEPINFRA_API_KEY", "")
    elif model_name.startswith("botrun"):
        return os.getenv("BOTRUN_API_KEY", "")
    else:
        return ""


def get_base_url(model_name: str) -> str:
    if model_name in TAIDE_MODELS or model_name.startswith("taide/"):
        return os.getenv("TAIDE_BASE_URL", "")
    elif model_name.startswith("botrun"):
        return os.getenv("BOTRUN_BASE_URL", "")
    else:
        return ""


def get_custom_llm_provider(model_name: str) -> str:
    if model_name.startswith("botrun"):
        return "openai"
    else:
        return None


def get_model_name(model_name: str) -> str:
    if model_name.startswith("taide/"):
        return model_name.split("/")[1]
    else:
        return model_name
