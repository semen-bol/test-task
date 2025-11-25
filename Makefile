PROJECT_NAME := testtask
COMPOSE_FILES := -f deploy/compose.yaml
DOCKER_COMPOSE := docker compose -p $(PROJECT_NAME) $(COMPOSE_FILES)

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d