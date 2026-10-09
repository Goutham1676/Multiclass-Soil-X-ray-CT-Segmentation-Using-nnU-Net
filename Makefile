.PHONY: help init test check

help:
	@echo "init  - Create the Conda environment"
	@echo "test  - Run the tests"
	@echo "check - Show detailed test results"

init:
	conda env create -f environment.yml

test:
	python -m pytest

check:
	python -m pytest -v