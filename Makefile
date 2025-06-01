# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt
	pip install pyright

# Run tests
test:
	pytest -v

# Run tests with coverage report
test-cov:
	pytest --cov=./ --cov-report=term-missing --cov-report=html

# Run type checking with pyright
typecheck:
	pyright

# Lint code
lint:
	ruff check .

# Format code
format:
	ruff format .

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pyrightcache" -exec rm -r {} +
	rm -f .coverage coverage.xml
	rm -rf htmlcov/ .pytest_cache/ .ruff_cache/

.PHONY: install-dev test test-cov typecheck lint format clean