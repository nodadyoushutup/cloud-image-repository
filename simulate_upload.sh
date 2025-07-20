#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   upload.sh <path-to-image-file> [destination-url]
# Example:
#   upload.sh /tmp/foo.png
#   upload.sh /tmp/foo.png https://my.api/upload

FILE="$1"
DEST="${2:-http://localhost:3918/upload}"

if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "Usage: $0 <path-to-image-file> [destination-url]" >&2
  exit 1
fi

if [[ -z "${CLOUD_REPOSITORY_APIKEY:-}" ]]; then
  echo "Error: CLOUD_REPOSITORY_APIKEY environment variable not set" >&2
  exit 1
fi

echo "Uploading '${FILE}' → ${DEST}"
# -s: silent, -w: append HTTP code on its own line, -S: show error on failure
# capture both body+code, so we can split them
response="$(curl -sS -H "CLOUD-REPOSITORY-APIKEY: ${CLOUD_REPOSITORY_APIKEY}" \
    -F "file=@${FILE}" \
    -w "\n%{http_code}" \
    "${DEST}")" || {
  echo "Error: curl invocation failed" >&2
  exit 1
}

# separate body vs status
http_code="${response##*$'\n'}"
body="${response%$'\n'*}"

if [[ "$http_code" =~ ^2 ]]; then
  echo "✅ Upload succeeded (HTTP ${http_code})"
  echo "Response body:"
  echo "$body"
  exit 0
else
  echo "❌ Upload failed (HTTP ${http_code})" >&2
  echo "Response body:" >&2
  echo "$body" >&2
  exit 1
fi
