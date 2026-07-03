# Transformer Serve

Configurable inference API for Hugging Face text-generation models. Swap models via env vars — no code changes.

**Docker Hub:** https://hub.docker.com/r/ssnym/transformer-serve

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
{"output": "generated text here"}
```

## API — `GET /health`

Returns runtime info about the loaded model and device.

Response:
```json
{
  "status": "OK",
  "uptime_seconds": 10.93,
  "device": "cpu",
  "device_type": "cpu",
  "model_name": "google/flan-t5-small",
  "model_type": "t5",
  "num_parameters": 76961152,
  "configured_model_type": "seq2seq"
}
```

## Supported Model Types
- `seq2seq`  — encoder-decoder models (e.g. `google/flan-t5-small`)
- `causal` — decoder-only model (e.g. `gpt2`, `microsoft/phi-2`)

