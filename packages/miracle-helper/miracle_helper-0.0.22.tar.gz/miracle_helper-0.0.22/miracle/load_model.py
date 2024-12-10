import os
from typing import Optional, Literal

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings

class MIRACLEModelFactory:
    @staticmethod
    def get_anthropic_model(
        model_name: Literal["haiku", "sonnet", "opus"] = "sonnet",
        temperature: float = 0.1,
        max_tokens: int = 8192,
        max_retries: int = 3,
        timeout: Optional[float] = None,
        streaming: bool = False,
        api_key: Optional[str] = None,
    ) -> ChatAnthropic:
        """Load the Anthropic model easily. You can freely revise it to make it easier to use."""

        model_mapping = {
            "sonnet": "claude-3-5-sonnet-20241022",
            "haiku": "claude-3-5-haiku-20241022",
            "opus": "claude-3-opus-latest"
        }

        anthropic_api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not anthropic_api_key:
            raise ValueError("Anthropic API key not found. Please provide it either through the api_key parameter or set it as an environment variable 'ANTHROPIC_API_KEY'")

        return ChatAnthropic(
            model=model_mapping[model_name],
            temperature=temperature,
            max_tokens=max_tokens,
            anthropic_api_key=anthropic_api_key,
            default_request_timeout=timeout,
            max_retries=max_retries,
            default_headers={"anthropic-beta": "prompt-caching-2024-07-31, pdfs-2024-09-25"},
            streaming=streaming
        )

    @staticmethod
    def get_openai_model(
        model_name: Literal['gpt-4o-mini', 'gpt-4o', 'chatgpt-4o-latest'] = "gpt-4o",
        temperature: float = 0.1,
        max_tokens: int = 8192,
        max_retries: int = 3,
        streaming: bool = False,
        api_key: Optional[str] = None,
    ) -> ChatOpenAI:
        model_mapping = {
            "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
            "gpt-4o": "gpt-4o-2024-08-06",
            "chatgpt-4o-latest": "chatgpt-4o-latest"
        }

        openai_api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please provide it either through the api_key parameter or set it as an environment variable 'OPENAI_API_KEY'")

        return ChatOpenAI(
            model_name=model_mapping[model_name],
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            openai_api_key=openai_api_key,
            streaming=streaming
        )

    @staticmethod
    def get_openai_embedding_model(
        model_name: Literal['small', 'large'] = 'small',
        api_key: Optional[str] = None,
    ) -> OpenAIEmbeddings:
        """Load the OpenAI embedding model easily. You can freely revise it to make it easier to use."""
        model_mapping = {
            "small": "text-embedding-3-small",
            "large": "text-embedding-3-large"
        }

        openai_api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please provide it either through the api_key parameter or set it as an environment variable 'OPENAI_API_KEY'")

        return OpenAIEmbeddings(
            model=model_mapping[model_name],
            openai_api_key=openai_api_key
        )

    @staticmethod
    def get_voyage_embedding_model(
        model_name: Literal["voyage-3", "voyage-3-lite", "voyage-finance-2", "voyage-multilingual-2", "voyage-code-2"] = "voyage-3",
        api_key: Optional[str] = None,
    ) -> VoyageAIEmbeddings:

        voyage_api_key = api_key or os.getenv('VOYAGE_API_KEY')
        if not voyage_api_key:
            raise ValueError("Voyage API key not found. Please provide it either through the api_key parameter or set it as an environment variable 'VOYAGE_API_KEY'")

        return VoyageAIEmbeddings(
            model=model_name,
            voyage_api_key=voyage_api_key
        )

