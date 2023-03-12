install:
	python -m pip install --upgrade pip &&\
		python -m pip install .

dev:
	python -m pip install --upgrade pip &&\
		python -m pip install -e .[dev]

test:
	pytest .

format:
	black .

lint:
	black . --check
	ruff .
	mypy .

check: lint test
