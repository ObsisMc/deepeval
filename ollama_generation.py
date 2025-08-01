import functools
from typing import Optional, Tuple, List, Union, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult
from deepeval.models import DeepEvalBaseLLM, DeepEvalBaseEmbeddingModel, OllamaEmbeddingModel
from deepeval.metrics.utils import trimAndLoadJson
from langchain_community.callbacks import get_openai_callback
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
import os
from config import CustomConfig

custom_config = CustomConfig()


def async_exception_handler(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        max_patient = 5
        cur_patient = 0
        return_e = None
        while cur_patient < max_patient:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                cur_patient += 1
                print(
                    f"Attempt {cur_patient} failed for function {func.__name__}: {e}"
                )
                return_e = e
        print(f"Function {func.__name__} failed after {max_patient} attempts.")
        raise return_e

    return wrapper


class CustomChatOpenAI(ChatOpenAI):
    format: str = None

    def __init__(self, format: str = None, **kwargs):
        super().__init__(**kwargs)
        self.format = format

    async def _acreate(
        self, messages: List[BaseMessage], **kwargs
    ) -> ChatResult:
        if self.format:
            kwargs["format"] = self.format
        return await super()._acreate(messages, **kwargs)


class OllamaLLM(DeepEvalBaseLLM):

    def __init__(
        self,
        model_name: str,
        base_url: str = custom_config.ollama_url,
        json_mode: bool = True,
        temperature: float = 0,
        *args,
        **kwargs,
    ):

        self.model_name = model_name
        self.base_url = base_url
        self.json_mode = json_mode
        self.temperature = temperature
        self.args = args
        self.kwargs = kwargs
        super().__init__(model_name)

    def load_model(self) -> CustomChatOpenAI:
        """Load and configure the Ollama model."""
        return CustomChatOpenAI(
            model_name=self.model_name,
            openai_api_key="ollama",
            base_url=self.base_url,
            format="json" if self.json_mode else None,
            temperature=self.temperature,
            *self.args,
            **self.kwargs,
        )

    def generate(
        self, prompt: str, schema: Any = None
    ) -> Union[Any, Tuple[str, float]]:

        chat_model = self.load_model()
        # print("generate")
        with get_openai_callback() as cb:
            res = chat_model.invoke(prompt)
            if schema is not None:
                try:
                    # Try to parse the response using the schema
                    data = trimAndLoadJson(res.content, None)
                    return schema(**data), 0.0
                except Exception:
                    # If schema parsing fails, return parsed JSON
                    return trimAndLoadJson(res.content, None)
            return res.content, 0.0

    @async_exception_handler
    async def a_generate(
        self, prompt: str, schema: Any = None
    ) -> Union[Any, Tuple[str, float]]:

        chat_model = self.load_model()
        with get_openai_callback() as cb:
            res = await chat_model.ainvoke(prompt)
            if schema is not None:
                try:
                    # Try to parse the response using the schema
                    data = trimAndLoadJson(res.content, None)
                    return schema(**data), 0.0
                except Exception:
                    # If schema parsing fails, return parsed JSON
                    return trimAndLoadJson(res.content, None)
            return res.content, 0.0

    def get_model_name(self) -> str:
        """Get the name of the current model."""
        return self.model_name

    @property
    def __class__(self):
        from deepeval.models import GPTModel

        return GPTModel


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

model_local = OllamaLLM(model_name=model_name)
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
        max_goldens_per_context=custom_config.max_goldens_per_context
    )

    df = synthesizer.to_pandas()
    df.insert(0, "id", df.index)
    df.drop(columns=["context"], inplace=True)

    # df.to_csv("goldens.csv", index=False)
    df.to_json(
        os.path.join(output_dir, f"goldens_{i}.json"),
        orient="records",
        indent=2,
        force_ascii=False,
    )
    print(f"Goldens generated and saved to {output_dir}/goldens_{i}.json")
