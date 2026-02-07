.PHONY: install install-dev activate run clean format lint test check docker-build run-dev run docker-stop

DOCKER_IMG_NAME = findtech
CONTAINER_NAME = findtech-app

install:
	@echo "Install dependencies for production..."
	@poetry install --without dev

install-dev:
	@poetry install

docker-build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMG_NAME) .

run-dev:
	@echo "Running findtech-app dev mode..."
	docker run --rm -p 8501:8501 \
		-v "$$(pwd)/src:/app/src" \
		--env-file .env \
		--name $(CONTAINER_NAME)-dev \
		$(DOCKER_IMG_NAME) \
		streamlit run main.py --server.runOnSave=true --server.fileWatcherType=poll

run:
	@echo "Running findtech-app production mode..."
	docker run --rm -p 8501:8501 \
		--env-file .env \
		--name $(CONTAINER_NAME) \
		$(DOCKER_IMG_NAME) 


docker-stop:
	@echo "Stopping and clean containers"
	docker stop $(CONTAINER_NAME) || true
	docker stop $(CONTAINER_NAME)-dev || true
	docker rm $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME)-dev || true


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

lint:
	@echo "\nCheck ruff and black linting..."
	@poetry run ruff check src scraper tests
	@poetry run black --check src scraper tests
	@echo "\nCheck mypy type..."
	@poetry run mypy src scraper tests

format:
	@echo "Fix formatting with ruff and black..."
	@poetry run ruff check --fix scraper src scraper tests
	@poetry run black src scraper tests

test: 
	@echo "\nRun all test.."
	@poetry run pytest -v

check: format lint test

