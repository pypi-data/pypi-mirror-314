# from haizelabs.logger import trace


from haizelabs.client import HaizeClient
from openai.types.chat import ChatCompletionMessageParam
import requests
import os


url = "https://api.haizelabs.com/"


from haizelabs.client import HaizeClient
from openai.types.chat import ChatCompletionMessageParam


def inference(content: list[ChatCompletionMessageParam]) -> str:
    return "I am a language model"


client = HaizeClient(
    api_key="hl_8399b61b30f75a12289bf3f6deaf7ae7e9e5d8b03609f0ed7ddc54500a2b4303"
)

result = client.judges.call(
    messages=[{"role": "user", "content": "fuck you!"}],
    judge_ids=[
        "f96d2d04-a348-47fc-8ce7-e553cd71a3bc",
    ],
)

print(result)
