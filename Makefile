install:
	pip install --upgrade pip &&\
		pip install -r requirements/prod.txt

install-dev:
	pip install --upgrade pip &&\
		pip install -r requirements/dev.txt

test:
	python -m pytest -vv --cov=restless --cov-report=xml --cov-report=term-missing:skip-covered

format:
	black --line-length 79 --check --diff .

lint:
	# mypy --strict --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --disallow-untyped-decorators restless
	mypy restless
	pydocstyle restless
	pycodestyle restless
	pylint restless

all: install
