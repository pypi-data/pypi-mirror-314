# LYMT: Let Your Model Think

Maximize the model's thinking process.

> This project was inspired by the [Thinking-Claude](https://github.com/richards199999/Thinking-Claude) project by richards199999 to **maximize the thought process of various LLM models.**
> Also he's developing Chrome Extension. If you're interested, please visit that repository. **Thank you for the good prompt!**

## Supporting Models

- OpenAI
- Ollama
- Anthropic

## Examples

```python
from lymt.models.openai_model import OpenAIModel

lymt = OpenAIModel(api_key="glhf_a9b94625dc0b8892075972b6513fb815", base_url="https://glhf.chat/api/openai/v1")

print(lymt.prompt.list())

content = "3.90 - 3.11 = x, solve for x"

response = lymt.chat.create(
    model="hf:meta-llama/Meta-Llama-3.1-405B-Instruct",
    prompt_name="o1-heavy.txt",
    content=content,
    repeat=10,
)

print(response)

```