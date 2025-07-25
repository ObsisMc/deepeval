import functools
from typing import Tuple, List, Union, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult
from deepeval.models import (
    DeepEvalBaseLLM,
    DeepEvalBaseEmbeddingModel,
    OllamaEmbeddingModel,
)
from dotenv import load_dotenv
import os

load_dotenv()


class CustomOllamaEmbeddingModel(OllamaEmbeddingModel):
    def __init__(self, *args, **kwargs):
        self.ip = os.environ.get("OLLAMA_EMBEDDING_IP", "localhost")
        self.port = os.environ.get("OLLAMA_EMBEDDING_PORT", "11434")
        self.base_url = f"http://{self.ip}:{self.port}"
        model_name = os.environ.get("OLLAMA_EMBEDDING_MODEL")
        self.api_key = os.environ.get("OLLAMA_EMBEDDING_API_KEY")

        self.args = args
        self.kwargs = kwargs
        DeepEvalBaseEmbeddingModel.__init__(self, model_name)


embedder = CustomOllamaEmbeddingModel()
print(embedder.embed_text("Hello world!"))  # Example usage of the embedder
