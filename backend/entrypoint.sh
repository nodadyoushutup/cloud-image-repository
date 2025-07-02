#!/usr/bin/env bash
set -eo pipefail

echo "::CIR_ENTRYPOINT_START::"
echo $DEV_MODE
cd "$(dirname "$0")"
export PYTHONPATH="/app:$PYTHONPATH"

if [ -f .env ]; then
  echo "📦 Loading environment variables from .env"
  while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue

    key="$(echo -n "$key" | xargs)"
    value="$(echo -n "$value" | xargs)"

    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"

    export "$key=$value"
    echo "🔧 $key=$value"
  done < .env
fi

if [ -d venv ]; then
  echo "🐍 Activating Python virtual environment from ./venv"
  source venv/bin/activate
  # pip install -r requirements.txt
fi

echo "🚀 Starting backend via python run.py with debugpy"
if [[ "${DEV_MODE}" == "true" ]]; then
  echo "⚙️ DEV_MODE: launching via python run.py with debugpy"
  python3 -u -m debugpy \
    --listen 0.0.0.0:5678 \
    ./run.py &
  BACKEND_PID=$!
  sleep 1
  echo "::CIR_BACKEND_RUNNING::"
  wait $BACKEND_PID
else
  echo "🔧 PROD_MODE: launching via Gunicorn"
  gunicorn run:app \
    --preload \
    -w 1 \
    -b 0.0.0.0:5000 &
  BACKEND_PID=$!
  sleep 1
  echo "::CIR_BACKEND_RUNNING::"
  wait $BACKEND_PID
fi