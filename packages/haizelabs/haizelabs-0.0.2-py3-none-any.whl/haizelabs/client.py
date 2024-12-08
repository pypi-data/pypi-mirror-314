from haizelabs_api import HaizeLabs as HaizeLabsAPI
from haizelabs.auth import get_user_id

import haizelabs.services as services
import os


class HaizeClient:
    def __init__(self, base_url: str = None, api_key: str = None):
        if not base_url and not (base_url := os.environ.get("HAIZE_LABS_BASE_URL")):
            base_url = f"https://api.haizelabs.com"

        if not api_key and not (api_key := os.environ.get("HAIZE_LABS_API_KEY")):
            raise Exception(
                "HAIZE_LABS_API_KEY not found. Generate an api key on https://platform.haizelabs.com/app/settings and save as HAIZE_API_KEY in your enviornment"
            )

        self.user_id = get_user_id(api_key, base_url)
        self.base_url = base_url
        self.api_key = api_key
        self.api_client = HaizeLabsAPI(base_url=base_url)
        self.judges = services.JudgesService(
            api_key=api_key, user_id=self.user_id, api_client=self.api_client
        )
        self.testing = services.TestingService(
            api_key=api_key, user_id=self.user_id, api_client=self.api_client
        )
