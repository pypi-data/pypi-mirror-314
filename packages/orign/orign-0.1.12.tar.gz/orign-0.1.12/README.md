# orign-py

A Python client for [Orign](https://github.com/agentsea/orign)

## Installation

```bash
pip install orign
```

Install the Orign CLI

```sh
curl -fsSL -H "Cache-Control: no-cache" https://storage.googleapis.com/orign/releases/install.sh | bash
```

Login to Orign

```sh
$ orign login
```

## Usage

Get a list of available models

```sh
$ orign get models
```

### Chat

Define which model we would like to use

```python
from orign import ChatModel

model = ChatModel(model="allenai/Molmo-7B-D-0924", provider="vllm")
```

Open a socket connection to the model

```python
model.connect()
```

Chat with the model

```python
model.chat(msg="What's in this image?", image="https://tinyurl.com/2fz6ms35")
```

Stream tokens from the model

```python
for response in model.chat(msg="What is the capital of France?", stream_tokens=True):
    print(response)
```

Send a thread of messages to the model

```python
model.chat(prompt=[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"},
    {"role": "user", "content": "When was it built?"}
])
```

Send a batch of threads to the model

```python
model.chat(batch=[
    [{"role": "user", "content": "What is the capital of France?"}, {"role": "assistant", "content": "Paris"}, {"role": "user", "content": "When was it built?"}],
    [{"role": "user", "content": "What is the capital of Spain?"}, {"role": "assistant", "content": "Madrid"}, {"role": "user", "content": "When was it built?"}]
]):
```

Use the async API

```python
from orign import AsyncChatModel

model = AsyncChatModel(model="allenai/Molmo-7B-D-0924", provider="vllm")
await model.connect()

async for response in model.chat(
    msg="What is the capital of france?", stream_tokens=True
):
    print(response)
```

### Embeddings
Define which model we would like to use

```python
from orign import EmbeddingModel

model = EmbeddingModel(provider="sentence-tf", model="clip-ViT-B-32")
```

Embed a text

```python
model.embed(text="What is the capital of France?")
```

Embed an image

```python
model.embed(image="https://example.com/image.jpg")
```

Embed text and image

```python
model.embed(text="What is the capital of France?", image="https://example.com/image.jpg")
```

Use the async API

```python
from orign import AsyncEmbeddingModel

model = AsyncEmbeddingModel(provider="sentence-tf", model="clip-ViT-B-32")
await model.connect()

await model.embed(text="What is the capital of France?")
```

### OCR

Define which model we would like to use

```python
from orign import OCRModel

model = OCRModel(provider="easyocr")
```

Detect text in an image

```python
model.detect(image="https://example.com/image.jpg")
```

Use the async API

```python
from orign import AsyncOCRModel

model = AsyncOCRModel(provider="doctr")
await model.connect()

await model.detect(image="https://example.com/image.jpg")
```

## Examples

See the [examples](examples) directory for more usage examples.
