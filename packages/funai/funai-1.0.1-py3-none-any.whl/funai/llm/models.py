from funsecret.secret import read_cache_secret
from funutil import getLogger
from openai import OpenAI
from openai.types.chat import ChatCompletion

logger = getLogger("funai")


class BaseModel:
    llm_provider = "openai"

    def __init__(self, *args, **kwargs):
        self.client = None
        self.model_name = None

    def instance(self, api_key, model_name, base_url, *args, **kwargs):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        return self

    def chat(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model_name, messages=[{"role": "user", "content": prompt}]
        )
        content = ""
        if response:
            if isinstance(response, ChatCompletion):
                content = response.choices[0].message.content
            else:
                logger.error(
                    f'[{self.llm_provider}] returned an invalid response: "{response}", please check your network '
                    f"connection and try again."
                )
        else:
            logger.error(
                f"[{self.llm_provider}] returned an empty response, please check your network connection and try again."
            )
        return content.replace("\n", "")


class Moonshot(BaseModel):
    llm_provider = "moonshot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def instance(
        self,
        api_key=None,
        model_name="moonshot-v1-8k",
        base_url="https://api.moonshot.cn/v1",
        *args,
        **kwargs,
    ):
        api_key = api_key or read_cache_secret("funai", "moonshot", "api_key")
        return super().instance(
            api_key=api_key, model_name=model_name, base_url=base_url, *args, **kwargs
        )


class Deepseek(BaseModel):
    llm_provider = "deepseek"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def instance(
        self,
        api_key=None,
        model_name="deepseek-chat",
        base_url="https://api.deepseek.com",
        *args,
        **kwargs,
    ):
        api_key = api_key or read_cache_secret("funai", "deepseek", "api_key")
        return super().instance(
            api_key=api_key, model_name=model_name, base_url=base_url, *args, **kwargs
        )


def get_model(provider, api_key=None):
    if provider == "moonshot":
        return Moonshot().instance(api_key=api_key)
    elif provider == "deepseek":
        return Deepseek().instance(api_key=api_key)
    else:
        logger.error(f'unsupported provider: "{provider}"')
