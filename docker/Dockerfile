FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y \
    curl \
    gnupg \
    python3 python3-pip python3-dev \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/ ./backend/
RUN mkdir -p /app/public
COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN pip3 install --no-cache-dir --break-system-packages -r backend/requirements.txt

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]