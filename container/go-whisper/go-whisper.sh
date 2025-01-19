# When using a NVIDIA GPU
docker run \
  --name whisper-server --rm \
  --runtime nvidia --gpus all \
  -v whisper:/data -p 8080:80 \
  ghcr.io/mutablelogic/go-whisper:latest

