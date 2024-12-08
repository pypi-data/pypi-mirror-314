from typing import Callable, List
from haizelabs_api import HaizeLabs as HaizeLabsAPI

import time
import warnings


class TestingService:
    def __init__(self, api_key: str, user_id: str, api_client: HaizeLabsAPI):
        self.api_client = api_client
        self.user_id = user_id
        self.headers = {"x-api-key": api_key}

    def red_team(
        self,
        behaviors: List[str],
        inference_function: Callable,
        judge_ids: List[str],
        user_id: str = None,
        name: str = None,
    ):
        print(f"Starting red teaming run ({len(behaviors)} behaviors)...")

        # Start red teaming job
        start_response = self.api_client.testing.start(
            test_data={
                "name": name,
                "user_id": user_id,
                "test_type": "RED_TEAMING",
                "behaviors": [{"description": b} for b in behaviors],
                "detector_ids": judge_ids,
            }
        )

        test_id = start_response.test_id

        if start_response.status == "ERROR":
            raise Exception("Error starting experiment run.")

        content_count = 0
        processed_content_ids = []
        update_content_response = []

        # Poll until red teaming run is complete
        while True:
            # Check for and upload awaiting response content
            with (
                warnings.catch_warnings()
            ):  # Ignore pydantic warning about content type
                warnings.simplefilter("ignore")
                update_response = self.api_client.testing.update(
                    test_id=test_id, contents=update_content_response
                )

            if update_response.status in ["COMPLETE", "ERROR"]:
                break

            # Generate responses to awaiting responses content
            update_content_response = []
            for content in update_response.contents:
                if (
                    content.status == "AWAITING_RESPONSE"
                    and content.id not in processed_content_ids
                ):
                    processed_content_ids.append(content.id)
                    content_output = inference_function(content.input_messages)
                    content.output_messages = [
                        {"role": "assistant", "content": content_output}
                    ]
                    content.status = "ANALYZING_RESPONSE"
                    content_count += 1
                    update_content_response.append(content)

            # Sleep for a small amount of time
            time.sleep(0.2)

        print(f"{content_count} inputs tested.")
        print("Red teaming run completed.")

    def experiment(
        self,
        dataset_id: str,
        inference_function: Callable,
        judge_ids: List[str],
        user_id: str = None,
        name: str = None,
    ):
        print(f"Starting experiment run (dataset id: {dataset_id})...")

        # Start red teaming job
        start_response = self.api_client.testing.start(
            test_data={
                "name": name,
                "user_id": user_id,
                "test_type": "EXPERIMENT",
                "dataset_id": dataset_id,
                "detector_ids": judge_ids,
            }
        )

        test_id = start_response.test_id

        if start_response.status == "ERROR":
            raise Exception("Error starting experiment run.")

        content_count = 0
        processed_content_ids = []
        update_content_response = []

        # Poll until red teaming run is complete
        while True:
            # Check for and upload awaiting response content
            with (
                warnings.catch_warnings()
            ):  # Ignore pydantic warning about content type
                warnings.simplefilter("ignore")
                update_response = self.api_client.testing.update(
                    test_id=test_id, contents=update_content_response
                )

            if update_response.status in ["COMPLETE", "ERROR"]:
                break

            # Generate responses to awaiting responses content
            update_content_response = []
            for content in update_response.contents:
                if (
                    content.status == "AWAITING_RESPONSE"
                    and content.id not in processed_content_ids
                ):
                    processed_content_ids.append(content.id)
                    content_output = inference_function(content.input_messages)
                    content.output_messages = [
                        {"role": "assistant", "content": content_output}
                    ]
                    content.status = "ANALYZING_RESPONSE"
                    content_count += 1
                    update_content_response.append(content)

            # Sleep for a small amount of time
            time.sleep(0.2)

        print(f"{content_count} inputs tested.")
        print("Experiment run completed.")
