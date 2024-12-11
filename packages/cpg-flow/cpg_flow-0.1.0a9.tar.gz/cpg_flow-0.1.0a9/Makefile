# Environment Setup
venv:
	uv sync

init: venv
	pre-commit install
	pre-commit install --hook-type commit-msg

# Actions
test:
	coverage run -m pytest tests --junitxml=test-execution.xml

clean:
	rm -rf build dist *.egg-info
	rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__
	rm -rf src/*.egg-info src/*/*.egg-info src/*/*/*.egg-info

ci-build: clean
	python -m pip install build "setuptools>=42" setuptools-scm wheel
	SETUPTOOLS_SCM_PRETEND_VERSION="$$NEW_VERSION" python -m build --sdist --wheel

build: clean
	uv build --sdist --wheel

install-build: build
	uv pip install dist/*.whl

install-local:
	uv install -e .

upload: clean build
	uv run twine check dist/*
	uv run twine upload -r testpypi dist/*

.PHONY: venv init test clean ci-build build install-build install-local upload
