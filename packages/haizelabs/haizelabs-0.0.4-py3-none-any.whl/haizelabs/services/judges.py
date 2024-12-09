from haizelabs_api import HaizeLabs as HaizeLabsAPI
from haizelabs_api.types.judge_call_params import (
    ContentTestContentInputOutputMessage,
)

from typing import List


class JudgesService:
    def __init__(self, api_key: str, user_id: str, api_client: HaizeLabsAPI):
        self.api_client = api_client
        self.user_id = user_id
        self.headers = {"x-api-key": api_key}

    def call(
        self,
        messages: List[ContentTestContentInputOutputMessage],
        judge_ids: List[str],
    ):
        content = {
            "input_messages": messages,
            "user_id": self.user_id,
        }
        result = self.api_client.judges.call(
            judge_ids=judge_ids, extra_headers=self.headers, content=content
        )

        return result
