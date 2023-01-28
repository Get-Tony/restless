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
	mypy restless
	pycodestyle restless
	pydocstyle restless

all: install-dev test format lint
