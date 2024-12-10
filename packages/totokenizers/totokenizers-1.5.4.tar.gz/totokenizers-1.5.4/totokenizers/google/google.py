from typing import Literal, Sequence

import vertexai
from vertexai.preview.generative_models import GenerativeModel

from ..schemas import ChatMLMessage


class GeminiTokenizer:
    """
    Tokenizer for Google's Gemini models (Vertex AI API).

    WARNING: you neeed to set up Google Cloud authentication before using this tokenizer.
    See the references below for more information.
    - https://googleapis.dev/python/google-api-core/latest/auth.html
    - https://cloud.google.com/docs/authentication/application-default-credentials

    Args:
        model_name (str): The model name of the tokenizer.

    Reference for token count via SDK and REST API:
    - https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/get-token-count
    """
    def __init__(
        self,
        model_name: Literal[
            "gemini-pro",
            "gemini-pro-vision",
        ],
        project_id: str,
        location: str,
    ):
        # Initialize the Vertex AI API (gets Google credentials as well)
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(model_name)

    def encode(self, text: str) -> list[int]:
        raise NotImplementedError("Method unavailable for Google's Gemini models.")

    def count_tokens(self, text: str) -> int:
        response = self.model.count_tokens(text)
        return response.total_tokens

    def count_chatml_tokens(self, messages: Sequence[ChatMLMessage]) -> int:
        # Gemini uses "user"/"model" roles
        # TODO: find out how many tokens each turn in conversation has
        # We can infer the number of tokens for each turn based on the "count_tokens" method
        pass
