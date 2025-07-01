#!/bin/bash

FILE="$1"
if [ -z "$FILE" ]; then
  echo "Usage: $0 <path-to-image-file>"
  exit 1
fi

curl -F "file=@${FILE}" http://localhost:5000/
