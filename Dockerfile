
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --index-url https://download.pytorch.org/whl/cpu torch==2.8.0+cpu && \
    pip install -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/


EXPOSE 8080

CMD ["sh", "-c", "streamlit run src/app.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.headless=true"]
