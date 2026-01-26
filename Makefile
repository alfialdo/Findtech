.PHONY: install install-dev activate run clean format lint test check

install:
	@echo "Install dependencies for production..."
	@poetry install --without dev

install-dev:
	@poetry install

run:
	poetry run python -m src.main

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

