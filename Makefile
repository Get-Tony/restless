install:
	pip install --upgrade pip &&\
		pip install -r requirements/prod.txt

install-dev:
	pip install --upgrade pip &&\
		pip install -r requirements/dev.txt

test:
	python -m pytest -vv --cov=restless --cov-report term-missing

format:
	black --line-length 79 --check --diff .

lint:
	pylint restless
	# mypy --strict --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --disallow-untyped-decorators .
	mypy .
	pycodestyle restless
	pydocstyle restless

all: install
