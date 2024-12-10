"""
Pricing:
https://www-files.anthropic.com/production/images/model_pricing_dec2023.pdf

Model knowledge cutoff (Anthropic only mentions "early 2023"):
https://support.anthropic.com/en/articles/8114494-how-up-to-date-is-claude-s-training-data

Context and generation token limits:
https://docs.anthropic.com/claude/reference/input-and-output-sizes
"""

from ..model_info import ChatModelInfo, EmbeddingModelInfo, TextModelInfo

ANTHROPIC_CHAT_MODELS = {
    info.name: info
    for info in [
        ChatModelInfo(
            completion_token_cost=0.024,
            cutoff="2023-01-01",
            feature_flags=[],
            max_output_tokens=204_096,
            max_tokens=204_096,
            name="claude-2.1",
            prompt_token_cost=0.008,
        ),
        ChatModelInfo(
            completion_token_cost=0.0024,
            cutoff="2023-01-01",
            feature_flags=[],
            max_output_tokens=104_096,
            max_tokens=104_096,
            name="claude-instant-1.2",
            prompt_token_cost=0.0008,
        ),
    ]
}


ANTHROPIC_MODELS: dict[str, ChatModelInfo] = {**ANTHROPIC_CHAT_MODELS}
