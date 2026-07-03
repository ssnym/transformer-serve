# Transformer Serve

Configurable inference API for Hugging Face text-generation models. Swap models via env vars — no code changes.

**Live Demo:** [https://ssnym-transformer-serve.hf.space](https://ssnym-transformer-serve.hf.space)

**Docker Hub:** [https://hub.docker.com/r/ssnym/transformer-serve](https://hub.docker.com/r/ssnym/transformer-serve)

## Try it now — no setup required

The API is live. Run these directly:

```bash
curl https://ssnym-transformer-serve.hf.space/health
```

```bash
curl -X POST "https://ssnym-transformer-serve.hf.space/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain what is AI"}'
```

> Note: runs on free CPU hardware and sleeps after inactivity — first request after idle may take 30-60s to wake up.


## Features
- Serves any seq2seq or causal HF text-generation model
- Automatic CPU/GPU detection
- Configurable parameters `max_new_tokens`, `temperature`, `do_sample`
- Input validation
- Dockerized for    portable deployment

## Run Locally
```bash

git clone git@github.com:ssnym/transformer-serve.git

cd transformer-serve

pip install -r requirements.txt

uvicorn app:app --host 0.0.0.0 --port 8000
```

Test:
```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain what is AI"}'
```

## Docker Image

Currently ships a lightweight CPU-only image, built with `Dockerfile.cpu` (CPU-only torch build, ~1.2GB).

Build:
```bash
docker build -f Dockerfile.cpu -t transformer-serve:cpu .
```

Run (default model):
```bash
docker run -p 8000:8000 transformer-serve:cpu
```

Run (custom model):
```bash
docker run -p 8000:8000 -e MODEL_NAME="gpt2" -e MODEL_TYPE="causal" transformer-serve:cpu
```

## API — `POST /generate`

Request body:
```json
{
"prompt": "Explain what is AI",
"max_new_tokens": 50,
"temperature": 0.7,
"do_sample": false
}
```

Response:
```json
{"output": "Explain what is AI and how it works.\nArtificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, reason, and act like humans. It involves creating algorithms and models that can process large amounts of data, recognize patterns, make decisions, and perform tasks without explicit programming.\n\nThere are several types of AI:\n\n1. Narrow or Weak AI..."}
```

## API — `GET /health`

Returns runtime info about the loaded model and device.

```json
{
  "status": "OK",
  "device": "cpu",
  "model_name": "Qwen/Qwen2.5-1.5B-Instruct",
  "model_type": "qwen2",
  "num_parameters": 1543714304,
  "configured_model_type": "causal"
}
```

## Supported Model Types
- `seq2seq`  — encoder-decoder models (e.g. `google/flan-t5-small`)
- `causal` — decoder-only model (e.g. `gpt2`, `microsoft/phi-2`)

