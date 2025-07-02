from deepeval.synthesizer.config import ContextConstructionConfig
import os
from dotenv import load_dotenv

load_dotenv()
# print("Loading env", os.getenv("OLLAMA_URL"))


class CustomConfig:

    def __init__(self):
        self.include_expected_output: bool = bool(
            os.environ["INCLUDE_EXPECTED_OUTPUT"]
        )
        self.max_goldens_per_context: int = int(
            os.environ["MAX_GOLDENS_PER_CONTEXT"]
        )
        self.context_construction_config = (
            self.get_context_construction_config()
        )

        self.data_dir: str = os.environ["INPUT_DIR"]
        self.output_dir: str = os.environ["OUTPUT_DIR"]

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Ollama specific configurations
        self.ollama_url: str = os.environ.get("OLLAMA_URL", None)
        self.ollama_url = self.ollama_url.replace(
            r"\x3a", ":"
        )  # Fix for ":" encoding in vscode
        # print(f"Using Ollama URL: {self.ollama_url}")
        self.ollama_model: str = os.environ.get("OLLAMA_MODEL", None)
        self.ollama_model = self.ollama_model.replace(
            r"\x3a", ":"
        )  # Fix for ":" encoding in vscode

    def get_context_construction_config(self) -> ContextConstructionConfig:
        """Returns the configuration for context construction."""
        critic_model = None
        encoding = None
        max_contexts_per_document: int = int(
            os.environ["MAX_CONTEXTS_PER_DOCUMENT"]
        )
        min_contexts_per_document: int = int(
            os.environ["MIN_CONTEXTS_PER_DOCUMENT"]
        )
        max_context_length: int = int(os.environ["MAX_CONTEXT_LENGTH"])
        min_context_length: int = int(os.environ["MIN_CONTEXT_LENGTH"])
        chunk_size: int = int(os.environ["CHUNK_SIZE"])
        chunk_overlap: int = int(os.environ["CHUNK_OVERLAP"])
        context_quality_threshold: float = float(
            os.environ["CONTEXT_QUALITY_THRESHOLD"]
        )
        context_similarity_threshold: float = float(
            os.environ["CONTEXT_SIMILARITY_THRESHOLD"]
        )
        max_retries: int = int(os.environ["MAX_RETRIES"])
        embedder = os.environ["EMBEDDER"]
        return ContextConstructionConfig(
            critic_model=critic_model,
            encoding=encoding,
            max_contexts_per_document=max_contexts_per_document,
            min_contexts_per_document=min_contexts_per_document,
            max_context_length=max_context_length,
            min_context_length=min_context_length,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            context_quality_threshold=context_quality_threshold,
            context_similarity_threshold=context_similarity_threshold,
            max_retries=max_retries,
            embedder=embedder,
        )


if __name__ == "__main__":
    custom_config = CustomConfig()
