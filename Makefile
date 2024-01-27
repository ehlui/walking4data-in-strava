
APP_NAME= stravascraper
APP_VERSION=0.0.1

all: build run

allclean: cbuild run

build:
	@echo --- Building Docker Image ---
	@docker build -t $(APP_NAME):$(APP_VERSION) -f src/Dockerfile src/

cbuild:
	@echo --- Rebuilding Image ---
	@docker rmi -f $(APP_NAME):$(APP_VERSION)
	@docker build --no-cache -t $(APP_NAME):$(APP_VERSION) -f src/Dockerfile src/
	@docker rm -f $(APP_NAME) > /dev/null

run:
	@echo --- Running Image ---
	@docker run --name $(APP_NAME)   $(APP_NAME):$(APP_VERSION)