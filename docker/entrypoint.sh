#!/usr/bin/env bash
set -eo pipefail

echo "Starting entrypoint..."
echo "::CIR_ENTRYPOINT_START::"

to_lower() { echo "$1" | tr '[:upper:]' '[:lower:]'; }

should_run_backend=false

backend_pid=""

if [ -d "./backend" ]; then
    echo "Running backend"
    (cd /app/backend && /app/backend/entrypoint.sh) &
    backend_pid=$!
else
    echo "⚠️  Backend disabled or folder not found; skipping Flask."
fi

# Wait for any to exit if both running, or just run foreground if only one enabled
if [[ -n "$backend_pid" ]]; then
    echo "⏳ Backend running. Waiting for it to exit..."
    wait $backend_pid
else
    echo "❌ Backend not started."
    exit 1
fi

echo "✅ Booted!"