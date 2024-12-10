from typing import Optional


class TotokenizersError(Exception):
    pass


class TokenLimitExceeded(TotokenizersError):
    msg = "Token limit of {max_tokens} exceeded for model {model_name}. Actual tokens: {actual_tokens}."

    def __init__(self, max_tokens: int, model_name: str, actual_tokens: int, *args):
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.actual_tokens = actual_tokens
        msg = self.msg.format(
            max_tokens=max_tokens, model_name=model_name, actual_tokens=actual_tokens
        )
        super().__init__(msg, *args)


class BadFormatForModelTag(TotokenizersError):
    msg = "Bad format for model tag {model_tag}. Use: <model_provider>/<model_name>."

    def __init__(self, model_tag: str, *args):
        self.model_tag = model_tag
        msg = self.msg.format(model_tag=model_tag)
        super().__init__(msg, *args)


class ModelNotFound(TotokenizersError):
    msg1 = "Model {model_name} not found."
    msg2 = "Model {model_name} not found for provider {model_provider}."

    def __init__(self, model_name: str, model_provider: Optional[str] = None, *args):
        self.model_name = model_name
        self.model_provider = model_provider
        if model_provider is None:
            msg = self.msg1.format(model_name=self.model_name)
        else:
            msg = self.msg.format(
                model_name=self.model_name, model_provider=self.model_provider
            )
        super().__init__(msg, *args)


class ModelProviderNotFound(TotokenizersError):
    msg = "Model provider {model_provider}."

    def __init__(self, model_provider: str, *args):
        self.model_provider = model_provider
        msg = self.msg.format(model_provider=self.model_provider)
        super().__init__(msg, *args)


class ModelNotSupported(TotokenizersError):
    msg = "Model {model_name} was found, but it is not supported by totokenizers yet."

    def __init__(self, model_name: str, *args):
        self.model_name = model_name
        msg = self.msg.format(model_name=model_name)
        super().__init__(msg, *args)
