install:
	pip install --upgrade pip &&\
		pip install -r requirements/prod.txt

install-dev:
	pip install --upgrade pip &&\
		pip install -r requirements/dev.txt

test: lint
	python -m pytest -vv --cov=restless --cov-report term-missing

format:
	black --line-length 79 --check --diff .

lint: format
	# mypy --strict --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --disallow-untyped-decorators restless
	mypy restless
	pydocstyle restless
	pycodestyle restless
	pylint restless

all: install
