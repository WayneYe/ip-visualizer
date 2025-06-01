.PHONY: test test-cov install-dev clean

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run tests
	test:
	pytest -v

# Run tests with coverage report
test-cov:
	pytest --cov=./ --cov-report=term-missing --cov-report=html

# Clean up generated files
clean:
	rm -rf `find . -type d -name __pycache__`
	rm -f .coverage
	rm -f coverage.xml
	rm -rf htmlcov
	rm -rf .pytest_cache
