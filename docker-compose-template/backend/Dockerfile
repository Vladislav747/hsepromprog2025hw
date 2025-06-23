FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    apt-get install --no-install-recommends -y curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]
