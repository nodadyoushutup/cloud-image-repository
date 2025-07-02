FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y curl gnupg \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y \
      python3 python3-pip python3-dev \
      nodejs \
      git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/ ./backend/

COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN pip3 install --no-cache-dir --break-system-packages -r backend/requirements.txt

WORKDIR /app/frontend
RUN npm install
WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]