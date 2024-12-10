# totokenizers

A model-agnostic library to encode text into tokens and couting them using different tokenizers.

## install

`pip install totokenizers`

## usage

```python
from totokenizers.factories import TotoModelInfo, Totokenizer

model = "openai/gpt-3.5-turbo-0613"
desired_max_tokens = 250
tokenizer = Totokenizer.from_model(model)
model_info = TotoModelInfo.from_model(model)

thread_length = tokenizer.count_chatml_tokens(thread, functions)
if thread_length + desired_max_tokens > model_info.max_tokens:
    raise YourException(thread_length, desired_max_tokens, model_info.max_tokens)
```
