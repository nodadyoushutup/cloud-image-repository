#!/usr/bin/env bash
set -euo pipefail

echo "🚨 WARNING: This will remove ALL Docker containers, images, volumes, and networks!"
read -p "Are you sure you want to continue? [y/N]: " CONFIRM

if [[ "${CONFIRM,,}" != "y" ]]; then
  echo "❌ Aborted."
  exit 1
fi

echo "🛑 Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || true

echo "🧹 Removing all containers..."
docker rm -f $(docker ps -aq) 2>/dev/null || true

echo "🧼 Removing all images..."
docker rmi -f $(docker images -aq) 2>/dev/null || true

echo "🗑️ Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null || true

echo "🌐 Removing all networks (except default ones)..."
docker network rm $(docker network ls | awk '$2 != "bridge" && $2 != "host" && $2 != "none" {print $1}') 2>/dev/null || true

echo "🚿 Performing system prune (just in case)..."
docker system prune -a --volumes -f

echo "✅ Docker has been fully reset."