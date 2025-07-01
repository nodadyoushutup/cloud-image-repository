#!/bin/bash

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <path-to-image-file>"
  exit 1
fi

if [ -z "$CLOUD_REPOSITORY_APIKEY" ]; then
  echo "CLOUD_REPOSITORY_APIKEY environment variable not set"
  exit 1
fi

echo "CLOUD_REPOSITORY_APIKEY set as ${CLOUD_REPOSITORY_APIKEY}"
curl -H "CLOUD-REPOSITORY-APIKEY: ${CLOUD_REPOSITORY_APIKEY}" -F "file=@${FILE}" http://localhost:5000/
