# Transformer Serve

Configurable inference API for Hugging Face text-generation models.  Swap models via environment variables without changing application code.


**Live Demo:** [https://ssnym-transformer-serve.hf.space](https://ssnym-transformer-serve.hf.space)  
**Docker Hub:** [https://hub.docker.com/r/ssnym/transformer-serve](https://hub.docker.com/r/ssnym/transformer-serve)

<p align="center">
  <img src="assets/homepage.png"
       width="95%"
       alt="Transformer Serve running on Hugging Face Spaces">
</p>

## Try it now — no setup required

The API is running on a free CPU Space. Stream an answer token by token:

```bash
curl -N -X POST "https://ssnym-transformer-serve.hf.space/generate/stream" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain what is AI ?", "max_new_tokens": 60}'
```

Or open [the live demo](https://ssnym-transformer-serve.hf.space) in a browser for a chat UI.

> Note: runs on free CPU hardware and sleeps after inactivity. The first request after idle may take 30–60s to wake up.

## Run locally

```bash
git clone https://github.com/ssnym/transformer-serve.git
cd transformer-serve
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000` for the chat UI, or test the API:

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain what is AI"}'
```


## Run with the Docker image

```bash
docker pull ssnym/transformer-serve:latest
docker run -p 8000:8000 ssnym/transformer-serve:latest
```

The default model is `Qwen/Qwen2.5-0.5B-Instruct`. The image is about 700 MB, and the model (about 1 GB) downloads on first start.  

Use a different model

```bash
docker run -p 8000:8000 \
  -e MODEL_NAME="google/flan-t5-small" \
  -e MODEL_TYPE="seq2seq" \
  ssnym/transformer-serve:latest
```




### Build your own image

```bash
docker build -f Dockerfile.cpu -t transformer-serve:local .

docker run -p 8000:8000 transformer-serve:local
```

> Built with `Dockerfile.cpu` (CPU-only torch build). Default model is `Qwen/Qwen2.5-0.5B-Instruct` (~1GB) — first run downloads weights from Hugging Face Hub, so expect a few minutes on first start.


## API

### `POST /generate`

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain what AI is ?", "max_new_tokens": 120, "temperature": 0.7, "do_sample": true}'
```

Response:

```json
{"output": "Artificial intelligence is the field of building systems that..."}
```


### `POST /generate/stream`

Same request body as `/generate`, but the response streams as plain text, token by token.

```bash
curl -N -X POST "http://127.0.0.1:8000/generate/stream" \
  -H "Content-Type: application/json" \
  -d '{"prompt": Explain what AI is ?", "max_new_tokens": 60}'
```

`-N` turns off curl's buffering, so you see tokens as they arrive.


### `GET /health`

Returns runtime info about the loaded model and device.  

```json
{
  "status": "OK",
  "device": "cpu",
  "device_type": "cpu",
  "model_name": "Qwen/Qwen2.5-0.5B-Instruct",
  "model_type": "qwen2",
  "num_parameters": 494032768,
  "configured_model_type": "causal",
  "chat_template": true
}
```

Omitted request fields use the defaults in `app.py`. With `do_sample` set to `false`, decoding is greedy and `temperature` has no effect.  

## Features
- Supports - Causal (decoder-only) and seq2seq (encoder-decoder) Hugging Face models
- Chat-template support for instruct models
- Streaming and one-shot responses
- Configurable `max_new_tokens`, `temperature`, and `do_sample`
- Automatic CPU/GPU detection
- Built-in chat UI at `/`
- Dockerized, and deployable to Hugging Face Spaces

## Supported Model Types

- `causal` — decoder-only models (e.g. `Qwen/Qwen2.5-0.5B-Instruct`, `gpt2`, `microsoft/phi-2`)
- `seq2seq` — encoder-decoder models (e.g. `google/flan-t5-small`)

