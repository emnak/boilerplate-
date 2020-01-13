install: install-requirements install-git-hooks

test:
	ENVIRONMENT=test python -m pytest -vv --cov-report term-missing --no-cov-on-fail --cov=src/
lint:
	pylint pipelines/ src/ utils/ --ignored-modules=tensorflow.keras

black:
	black .

install-requirements:
	pip install git+ssh://git@github.com/sicara/pipeline.git@v0.11.2
	pip install -r dev_requirements.txt

install-git-hooks:
	pre-commit install

doc-style:
	pydocstyle --config=./setup.cfg src
