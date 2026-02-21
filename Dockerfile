# Build command: docker build -t blk-hacking-ind-openai-codex .
# Linux base image choice: python:3.11-slim (Debian-based) gives a minimal, secure Linux footprint with broad wheel compatibility.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 5477

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5477"]
