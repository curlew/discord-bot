# syntax=docker/dockerfile:1

FROM python:3.8-slim-bookworm
LABEL org.opencontainers.image.source=https://github.com/curlew/discord-bot

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
