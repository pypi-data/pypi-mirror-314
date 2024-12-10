"""
https://github.com/Significant-Gravitas/Auto-GPT/blob/3a2d08fb415071cc94dd6fcee24cfbdd1fb487dd/autogpt/llm/base.py#L47
"""

from .model_info import ChatModelInfo, EmbeddingModelInfo, TextModelInfo

OPEN_AI_CHAT_MODELS = {
    info.name: info
    for info in [
        ChatModelInfo(
            completion_token_cost=0.0006,
            cutoff="2023-10-01",
            feature_flags=["functions", "tools", "json", "vision", "voice"],
            max_output_tokens=128_000,
            max_tokens=128_000,
            name="ft:gpt-4o-2024-08-06:osf-digital:revenue-cloud-4o:A5s5vXgB",
            prompt_token_cost=0.00015,
        ),
        ChatModelInfo(
            completion_token_cost=0.0006,
            cutoff="2023-10-01",
            feature_flags=["functions", "tools", "json", "vision", "voice"],
            max_output_tokens=128_000,
            max_tokens=128_000,
            name="gpt-4o-mini-2024-07-18",
            prompt_token_cost=0.00015,
        ),
        ChatModelInfo(
            completion_token_cost=0.015,
            cutoff="2023-10-01",
            feature_flags=["functions", "tools", "json", "vision", "voice"],
            max_output_tokens=128_000,
            max_tokens=128_000,
            name="gpt-4o-2024-05-13",
            prompt_token_cost=0.005,
        ),
        ChatModelInfo(
            completion_token_cost=0.03,
            cutoff="2023-12-01",
            feature_flags=["functions", "tools", "json", "vision"],
            max_output_tokens=128_000,
            max_tokens=128_000,
            name="gpt-4-turbo-2024-04-09",
            prompt_token_cost=0.01,
        ),
        ChatModelInfo(
            completion_token_cost=0.03,
            cutoff="2023-12-01",
            feature_flags=["functions", "tools", "json"],
            max_output_tokens=4096,
            max_tokens=128_000,
            name="gpt-4-0125-preview",
            prompt_token_cost=0.01,
        ),
        ChatModelInfo(
            completion_token_cost=0.03,
            cutoff="2023-04-01",
            feature_flags=["functions", "tools", "json"],
            max_output_tokens=4096,
            max_tokens=128_000,
            name="gpt-4-1106-preview",
            prompt_token_cost=0.01,
        ),
        ChatModelInfo(
            completion_token_cost=0.03,
            cutoff="2023-04-01",
            feature_flags=["functions", "tools", "json", "vision"],
            max_output_tokens=4096,
            max_tokens=128000,
            name="gpt-4-1106-vision-preview",
            prompt_token_cost=0.01,
        ),
        ChatModelInfo(
            completion_token_cost=0.0015,
            cutoff="2021-09-01",
            feature_flags=["functions", "tools", "json"],
            max_output_tokens=4096,
            max_tokens=16_385,
            name="gpt-3.5-turbo-0125",
            prompt_token_cost=0.0005,
        ),
        ChatModelInfo(
            completion_token_cost=0.002,
            cutoff="2021-11-01",
            feature_flags=["functions", "tools", "json"],
            max_output_tokens=4096,
            max_tokens=16_385,
            name="gpt-3.5-turbo-1106",
            prompt_token_cost=0.001,
        ),
        ChatModelInfo(
            completion_token_cost=0.002,
            cutoff="2021-11-01",
            deprecated=True,
            max_output_tokens=4096,
            max_tokens=4096,
            name="gpt-3.5-turbo-0301",
            prompt_token_cost=0.0015,
        ),
        ChatModelInfo(
            completion_token_cost=0.002,
            cutoff="2021-11-01",
            deprecated=True,
            feature_flags=["functions"],
            max_output_tokens=4096,
            max_tokens=4096,
            name="gpt-3.5-turbo-0613",
            prompt_token_cost=0.0015,
        ),
        ChatModelInfo(
            completion_token_cost=0.004,
            cutoff="2021-11-01",
            deprecated=True,
            feature_flags=["functions"],
            max_output_tokens=16385,
            max_tokens=16385,
            name="gpt-3.5-turbo-16k-0613",
            prompt_token_cost=0.003,
        ),
        ChatModelInfo(
            completion_token_cost=0.06,
            cutoff="2021-11-01",
            deprecated=True,
            max_output_tokens=8192,
            max_tokens=8192,
            name="gpt-4-0314",
            prompt_token_cost=0.03,
        ),
        ChatModelInfo(
            completion_token_cost=0.06,
            cutoff="2021-11-01",
            deprecated=True,
            feature_flags=["functions"],
            max_output_tokens=8192,
            max_tokens=8192,
            name="gpt-4-0613",
            prompt_token_cost=0.03,
        ),
        ChatModelInfo(
            completion_token_cost=0.12,
            cutoff="2021-11-01",
            deprecated=True,
            max_output_tokens=32768,
            max_tokens=32768,
            name="gpt-4-32k-0314",
            prompt_token_cost=0.06,
        ),
        ChatModelInfo(
            completion_token_cost=0.12,
            cutoff="2021-11-01",
            max_tokens=32768,
            max_output_tokens=32768,
            name="gpt-4-32k-0613",
            prompt_token_cost=0.06,
            feature_flags=["functions"],
        ),
    ]
}

OPEN_AI_TEXT_MODELS = {
    info.name: info
    for info in [
        TextModelInfo(
            completion_token_cost=0.02,
            cutoff="2021-11-01",
            max_tokens=4096,
            name="text-davinci-003",
            prompt_token_cost=0.02,
        ),
        TextModelInfo(
            completion_token_cost=0.002,
            cutoff="2021-11-01",
            max_tokens=4096,
            name="gpt-3.5-turbo-instruct",
            prompt_token_cost=0.0015,
        ),
    ]
}

OPEN_AI_EMBEDDING_MODELS = {
    info.name: info
    for info in [
        EmbeddingModelInfo(
            cutoff="2021-11-01",
            default_dim=1536,
            supported_dim=[1536],
            max_tokens=8191,
            name="text-embedding-ada-002",
            prompt_token_cost=0.0001,
        ),
        EmbeddingModelInfo(
            cutoff="2021-11-01",
            default_dim=3072,
            supported_dim=[256, 1024, 3072],
            max_tokens=8191,
            name="text-embedding-3-large",
            prompt_token_cost=0.00013,
        ),
        EmbeddingModelInfo(
            cutoff="2021-11-01",
            default_dim=1536,
            supported_dim=[512, 1536],
            max_tokens=8191,
            name="text-embedding-3-small",
            prompt_token_cost=0.00002,
        ),
    ]
}

# Set aliases for rolling model IDs
chat_model_mapping = {
    "gpt-3.5-turbo": "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-16k-0613",
    "gpt-4": "gpt-4-0613",
    "gpt-4-turbo": "gpt-4-turbo-2024-04-09",
    "gpt-4-32k": "gpt-4-32k-0613",
    "gpt-4o": "gpt-4o-2024-05-13",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
}
for alias, target in chat_model_mapping.items():
    alias_info = ChatModelInfo(**OPEN_AI_CHAT_MODELS[target].__dict__)
    alias_info.name = alias
    OPEN_AI_CHAT_MODELS[alias] = alias_info


OPEN_AI_MODELS: dict[str, ChatModelInfo | EmbeddingModelInfo | TextModelInfo] = {
    **OPEN_AI_CHAT_MODELS,
    **OPEN_AI_TEXT_MODELS,
    **OPEN_AI_EMBEDDING_MODELS,
}
