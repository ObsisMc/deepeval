# Synthetic Data Generation Using LLM

> This project is based on [Deepeval](https://github.com/confident-ai/deepeval).

## Install

```shell
pip install -r requirements.txt
```

## Configuration

Please create a `.env` based on `.env.template`

By default, we use OpenAI's API so please set up your OpenAI API Key

```shell
OPENAI_API_KEY=<your_api_key>

```

If use Ollama for data generation, set up

```shell
OLLAMA_URL="http://localhost:11434/v1/"
OLLAMA_MODEL="llama3.2:1b"
```

If you didn't change the base url of Ollama previously, just keep the default value of `OLLAMA_URL`.

## Quick Start

### Use OpenAI API
We have provided a sample txt in the `data/` folder. After configuring the `OPENAI_API_KEY`, you can have a quick try by running

```shell
python openai_generation.py

```

The output format is like

```json
[
  {
    "id":0,
    "input":"A question.",
    "actual_output":null,
    "expected_output": "The response",
    "retrieval_context":null,
    "n_chunks_per_context":3,
    "context_length":1949,
    "evolutions":[
      "Hypothetical"
    ],
    "context_quality":null,
    "synthetic_input_quality":1.0,
    "source_file":".\/data\/vol1.txt"
  },
  ...
]

```

which is a list of Json object.

### Use Custom Chat/Critic Model (Ollama)

We also provide an example for custom chat models, especially for Ollama. After setting up Ollama's config, run

```shell
python ollama_generation.py

```

Pay attention: it only sets the chat/critic model be Ollama model, but the embedding model is still OpenAI's.

### Use Custom Embedding Model (Ollama)

Make sure you have the embedding model mentioned in the `.env.template`. Then run 

```python
python custom_embedder.py
```
