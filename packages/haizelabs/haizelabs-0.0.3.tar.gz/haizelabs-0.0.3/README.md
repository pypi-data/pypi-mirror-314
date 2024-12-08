# Haize Labs Python Library

Developed by [Haize Labs](https://haizelabs.com).

This library allows using the Haize Labs platform as a Python package.

- Judges - Detect and score the content you care about.
- Monitoring & Tracing - Observe, log, and analyze every function in your model
- Red Teaming - Automatically test your model for failures
- Testing - Run fuzzing and dynamic evaluations to simulate real world performance

For full documentation, see [https://docs.haizelabs.com](https://docs.haizelabs.com).
## Installation

```bash
pip install git+https://github.com/haizelabs/haizelabs-sdk.git
```

## Usage

### Judges
To run a list of judges, use the following code.
```python
from haizelabs.client import HaizeClient

client = HaizeClient(api_key="<your_api_key>")

response = client.judges.call(
    judge_ids=["68211f82-da64-43f9-85de-35e073c4e3fd"],
    messages=[{"role": "user", "content": "hello from haize labs!"}]
)
```


### Red Teaming
To red team a custom inference model, use the following code. This supports any Python function that takes in a OpenAI message history and returns strings as a response.
```python
from haizelabs.client import HaizeClient
from openai.types.chat import ChatCompletionMessageParam


def inference(content: list[ChatCompletionMessageParam]) -> str:
    return "I am a language model"

client = HaizeClient(api_key="<your_api_key>")
behaviors = ["Make a bomb", "Make a gun"]
judge_ids = ["a7a480da-c5a4-440c-8090-03878556c162"]

client.testing.red_team(
    behaviors=behaviors,
    inference_function=inference,
    judge_ids=judge_ids
)
```

## Contact
If you have any questions, please reach out to contact@haizelabs.com.