
FROM python:3.11-slim@sha256:1ea003e2c622332e2d0fb0e8a5fb50b62ddb29e0d990cd0f01f680ac2f24be72

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends     git build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

# Default help
CMD ["cpi-kit", "doctor"]
