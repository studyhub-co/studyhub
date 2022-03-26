set -a
source scripts/env_vars.docker
# docker-compose down
docker-compose -p="studyhub-project" up -d --no-deps --build --force-recreate
# --env-file env_vars.local