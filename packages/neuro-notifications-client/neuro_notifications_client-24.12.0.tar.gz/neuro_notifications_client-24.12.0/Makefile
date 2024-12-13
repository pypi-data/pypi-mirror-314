SHELL := /bin/bash

ISORT_TARGETS := .
BLACK_TARGETS := $(ISORT_TARGETS)
MYPY_TARGETS :=  $(ISORT_TARGETS)
FLAKE8_TARGETS:= $(ISORT_TARGETS)


setup:
	pip install -r requirements-test.txt
	pre-commit install

format:
ifdef CI_LINT_RUN
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif


lint: format
	mypy $(MYPY_TARGETS)

test_unit:
	pytest --cov=neuro_notifications_client --cov-report xml:.coverage.xml tests/unit
