.PHONY: install install-dev activate run clean format lint test check docker-build run-dev run-prod docker-stop

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

run-prod:
	@echo "Running findtech-app prod mode..."
	docker run --rm -p 8501:8501 \
		-v "$$(pwd)/src:/app/src" \
		--env-file .env \
		--name $(CONTAINER_NAME)-dev \
		--restart unless-stopped \ 
		$(DOCKER_IMG_NAME) \


docker-stop:
	@echo "Stopping and clean containers"
	docker stop $(CONTAINER_NAME) || true
	docker stop $(CONTAINER_NAME)-dev || true
	docker rm $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME)-dev || true


clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

lint:
	@echo -e "\nCheck ruff and black linting..."
	@poetry run ruff check src scraper tests
	@poetry run black --check src scraper tests
	@echo -e "\nCheck mypy type..."
	@poetry run mypy src scraper tests

format:
	@echo "Fix formatting with ruff and black..."
	@poetry run ruff check --fix scraper src scraper tests
	@poetry run black src scraper tests

test: 
	@echo -e "\nRun all test.."
	@poetry run pytest -v

check: format lint test

