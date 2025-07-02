from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
import os
from dotenv import load_dotenv

load_dotenv()


# synthesizer = Synthesizer()
# synthesizer.generate_goldens_from_docs(
#     document_paths=["example.txt"],
#     context_construction_config=ContextConstructionConfig(
#         # max_contexts_per_document=5,
#         # max_context_length=3,
#         # chunk_size=1024,
#         # context_quality_threshold=0.5,
#         max_contexts_per_document=2,
#         chunk_size=2048,
#     ),
# )


data_dir = "data"
synthesizer = Synthesizer()
synthesizer.generate_goldens_from_docs(
    document_paths=[
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(".txt")
    ][:1],
    context_construction_config=ContextConstructionConfig(
        max_contexts_per_document=2, chunk_size=2048
    ),
)

df = synthesizer.to_pandas()
df.insert(0, "id", df.index)
df.drop(columns=["context"], inplace=True)

# df.to_csv("goldens.csv", index=False)
df.to_json("goldens.json", orient="records", indent=2, force_ascii=False)
print("Goldens generated and saved to goldens.json")
