.PHONY: all test lint clean

all: lint test

test:
	python3.6 ktls.py
lint:
	flake8 ktls ktls.py https.py
clean:
