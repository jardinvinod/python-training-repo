IMAGE_NAME=ollama-streamlit-chat
TAR_FILE=jardinvinod_module7_06.tar


# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .


# Start containers using Docker Compose
up:
	docker compose up --build


# Start containers in background
up-d:
	docker compose up --build -d


# Stop containers
down:
	docker compose down


# Show running containers
status:
	docker compose ps


# Download Ollama model
model:
	docker exec -it ollama_module7_06 ollama pull qwen2.5:0.5b


# Export Docker image to .tar
save:
	docker save -o $(TAR_FILE) $(IMAGE_NAME)


# Load Docker image from .tar
load:
	docker load -i $(TAR_FILE)


# Build and save image
all: build save