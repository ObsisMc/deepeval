import functools
from typing import Optional, Tuple, List, Union, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult
from deepeval.models import (
    DeepEvalBaseLLM,
    DeepEvalBaseEmbeddingModel,
    OllamaEmbeddingModel,
    OllamaModel,
)
import logging
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential_jitter,
    RetryCallState,
    stop_after_attempt,
)
from deepeval.metrics.utils import trimAndLoadJson
from langchain_community.callbacks import get_openai_callback
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
import os
from config import CustomConfig
import re
import logging

custom_config = CustomConfig()
logging.basicConfig(level=logging.INFO)


# NOT USED, but can be used to remove thinking patterns from the text
def remove_thinking(res: str) -> str:
    """Remove thinking patterns from the text."""
    res = res.strip()
    # Remove thinking patterns like "thinking: " or "thinking: "
    res = re.sub(r"^<think>[\s\S]*?</think>", "", res, count=1)
    # Remove any trailing spaces or newlines
    return res


def log_after(retry_state):
    exception = retry_state.outcome.exception()
    logging.error(
        f"[Retry #{retry_state.attempt_number}] Exception: {exception!r}"
    )


class CustomOllamaModel(OllamaModel):
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = custom_config.ollama_url,
        temperature: float = 0,
        **kwargs,
    ):
        self.base_url = base_url
        self.model_name = model
        if temperature < 0:
            raise ValueError("Temperature must be >= 0.")
        self.temperature = temperature
        DeepEvalBaseLLM.__init__(self, self.model_name)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)

        # Wrap only callable methods from the superclass
        if (
            callable(attr)
            and not name.startswith("__")
            and hasattr(OllamaModel, name)
        ):

            # add retry logic to all methods except built-in ones
            return retry(
                # wait=wait_exponential_jitter(
                #     initial=1, exp_base=2, jitter=2, max=10
                # ),
                stop=stop_after_attempt(5),
                retry=retry_if_exception_type(Exception),
                after=log_after,
            )(attr)

        return attr


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


model_name = custom_config.ollama_model  # or any other model you want to use
data_dir = custom_config.data_dir
output_dir = custom_config.output_dir
context_construction_config = custom_config.context_construction_config

model_local = CustomOllamaModel(model=model_name)
embedder_local = CustomOllamaEmbeddingModel()
context_construction_config.embedder = embedder_local
context_construction_config.critic_model = model_local
print(context_construction_config)

document_paths = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.endswith(".txt")
]

for i, doc_path in enumerate(document_paths):
    synthesizer = Synthesizer(model=model_local)
    synthesizer.generate_goldens_from_docs(
        document_paths=[doc_path],
        context_construction_config=context_construction_config,
        max_goldens_per_context=custom_config.max_goldens_per_context,
    )

    df = synthesizer.to_pandas()

    logging.info(f"Generated {len(df)} goldens")
    df.drop_duplicates(subset=["input", "expected_output"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    logging.info(f"After deduplication, {len(df)} goldens remain")

    df.insert(0, "id", df.index)
    df.drop(columns=["context"], inplace=True)

    # df.to_csv("goldens.csv", index=False)
    df.to_json(
        os.path.join(output_dir, f"goldens_{i}.json"),
        orient="records",
        indent=2,
        force_ascii=False,
    )
    logging.info(
        f"Goldens generated and saved to {output_dir}/goldens_{i}.json"
    )
