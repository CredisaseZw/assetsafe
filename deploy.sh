#!/bin/bash
set -e 

#echo "Starting deployment at $(date)"

# Stash local changes
git stash

DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"
COMPOSE_FILE="docker-compose.prod.yml"

git pull origin "$DEPLOY_BRANCH"

# Bring down containers
docker compose -f "$COMPOSE_FILE" down --remove-orphans

docker compose -f "$COMPOSE_FILE" up -d --build

echo "Deployment completed at $(date)"
