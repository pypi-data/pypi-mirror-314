import requests
import os


def init_haizelabs():
    api_key = os.environ.get("HAIZE_API_KEY")

    if api_key is None:
        raise Exception(
            "HAIZE_API_KEY not found. Generate an api key on https://platform.haizelabs.com/app/settings and save as HAIZE_API_KEY in your enviornment"
        )

    return api_key


def get_user_id(api_key: str, base_url: str):
    response = requests.get(f"{base_url}/keys/get_user_id/{api_key}")
    if response.status_code != 200:
        raise Exception(
            "Error retreiving User. Make sure your api key is a valid api key from https://platform.haizelabs.com/app/settings"
        )
    user = response.json()
    return user
