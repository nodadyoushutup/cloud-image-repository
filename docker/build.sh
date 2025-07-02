#!/usr/bin/env bash
set -euo pipefail

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."

# Optional tag argument, default to publex:latest
TAG="${1:-publex:latest}"

echo "🛠️  Building Docker image '$TAG'…"

# 1) Build normally so you see all of Docker’s output
docker build \
  -f "$SCRIPT_DIR/Dockerfile" \
  -t "$TAG" \
  "$REPO_ROOT"

echo "✅ Build complete."

# 2) Get the full content-addressable ID (sha256:…)
FULL_ID=$(docker inspect --format='{{.Id}}' "$TAG")

# 3) Extract just the hex and take first 12 chars for the “short” ID
HEX=${FULL_ID#sha256:}
SHORT_ID=${HEX:0:12}

# 4) (Optionally) pull back the digest for immutable references
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$TAG" 2>/dev/null || true)

echo
echo "Full Image ID:    $FULL_ID"
echo "Short Image ID:   $SHORT_ID"
[ -n "$DIGEST" ] && echo "Image Digest:     $DIGEST"
echo "Image Tag:        $TAG"