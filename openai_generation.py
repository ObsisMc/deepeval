from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
import os
from config import CustomConfig

custom_config = CustomConfig()


data_dir = custom_config.data_dir
output_dir = custom_config.output_dir
output_file = os.path.join(output_dir, "goldens.json")


synthesizer = Synthesizer()
synthesizer.generate_goldens_from_docs(
    document_paths=[
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(".txt")
    ],
    include_expected_output=custom_config.include_expected_output,
    max_goldens_per_context=custom_config.max_goldens_per_context,
    context_construction_config=custom_config.context_construction_config,
)

df = synthesizer.to_pandas()
df.insert(0, "id", df.index)
df.drop(columns=["context"], inplace=True)

# df.to_csv("goldens.csv", index=False)
df.to_json(output_file, orient="records", indent=2, force_ascii=False)
print(f"Goldens generated and saved to {output_file}")
