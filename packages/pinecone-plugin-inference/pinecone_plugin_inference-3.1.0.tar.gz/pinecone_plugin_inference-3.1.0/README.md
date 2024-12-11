# Inference API plugin for python SDK

## Installation

The plugin is distributed separately from the core python sdk.

```
# Install the base python SDK, version 4.1.1 or higher
pip install pinecone-client

# And also the plugin functionality
pip install pinecone-plugin-inference
```

## Usage

Interact with Pinecone's Inference APIs, e.g. create embeddings (currently in preview).

Models currently supported:
- [multilingual-e5-large](https://arxiv.org/pdf/2402.05672)

## Generate embeddings
The following example highlights how to use an embedding model to generate embeddings for a list of documents and a 
user query, with the ultimate goal of retrieving similar documents from a Pinecone index.

```python
from pinecone import Pinecone

pc = Pinecone(api_key="<<PINECONE_API_KEY>>")
model = "multilingual-e5-large"

# Embed documents
text = [
    "Turkey is a classic meat to eat at American Thanksgiving.",
    "Many people enjoy the beautiful mosques in Turkey.",
]
text_embeddings = pc.inference.embed(
    model=model,
    inputs=text,
    parameters={"input_type": "passage", "truncate": "END"},
)

# <<Upsert documents into Pinecone index>>

# Embed query
query = ["How should I prepare my turkey?"]
query_embeddings = pc.inference.embed(
    model=model,
    inputs=query,
    parameters={"input_type": "query", "truncate": "END"},
)

# <<Send query to Pinecone index to retrieve similar documents>>
```
