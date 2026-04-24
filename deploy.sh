#!/bin/bash
set -e 

echo "Starting deployment at $(date)"

# Stash local changes
git stash

git pull origin main

docker system prune -f --volumes

# Bring down containers
docker compose down

docker compose up -d --build

echo "Deployment completed at $(date)"