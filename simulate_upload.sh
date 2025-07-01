#!/bin/bash

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <path-to-image-file>"
  exit 1
fi

if [ -z "$GH_TOKEN" ]; then
  echo "GH_TOKEN environment variable not set"
  exit 1
fi

echo "GH_TOKEN set as ${GH_TOKEN}"
curl -H "GITHUB-TOKEN: ${GH_TOKEN}" -F "file=@${FILE}" http://localhost:5000/
