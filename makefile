# Makefile
#
# This Makefile is used to manage the project.
#
# Usage:
#	make <options> <target>
#
# Targets:
#	all        Build the project
#	ver        Print project version and exit
#	clean      Clean the project
#	install    Install the project with default config
# 	install-prod
# 	           Install the project for production
#	install-dev
#	           Install the project for development
#	install-root
#	           Install the project root only
#	install-no-root
#	           Install the project dependencies only
#	build      Build the project
#	test       Run the tests
#	publish    Publish the project
#	deploy     Deploy the project (all publish)
#	lint       Lint the project

# Environment variables
VENV_DIR := .venv
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
PYTHON_VERSION := $(shell python -c "import platform; print(platform.python_version())")
PYTHON_MINOR := $(shell python -c "import platform; print(platform.python_version_tuple()[1])")

ifeq ($(shell test $(PYTHON_MINOR) -gt 10; echo $$?),0)
	TOMLLIB := tomllib
else
	TOMLLIB := tomli
endif


PROJECT_NAME := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
PROJECT_SRC := src/$(PROJECT_NAME)/
PROJECT_VERSION := $(shell python -c "import $(TOMLLIB);f=open('pyproject.toml', 'rb'); toml=tomllib.load(f); print(toml['tool']['poetry']['version'])")
PROJECT_OUTDIR := "./dist/v$(PROJECT_VERSION)"

PYTEST_ARGS := -v
MAX_LINE_LENGTH := 127
FLAKE8_EXCLUDE := $(VENV_DIR),*.bak,*.tmp
BUILD_ARGS := --outdir=$(PROJECT_OUTDIR)

ifeq ($(OS),Windows_NT)
	VENV_BIN_DIR := $(VENV_DIR)/Scripts
	VENV_PYTHON := $(VENV_BIN_DIR)/python.exe
else
	VENV_BIN_DIR := $(VENV_DIR)/bin
	VENV_PYTHON := $(VENV_BIN_DIR)/python3
endif

# Default target
.DEFAULT_GOAL := all

# Targets
venv: $(VENV_DIR)
all: clean venv install-dev lint test build clean
deploy: all publish

ver: pyproject.toml
	echo "$(PROJECT_NAME) v$(PROJECT_VERSION) on python v$(PYTHON_VERSION)"

clean:
	rm './poetry.lock'

install: pyproject.toml $(VENV_DIR)/
	poetry install

install-prod: pyproject.toml $(VENV_DIR)/
	poetry install --without=dev

install-dev: pyproject.toml $(VENV_DIR)/
	poetry install --with=dev

install-root: pyproject.toml $(VENV_DIR)/
	poetry install --only-root

install-no-root: pyproject.toml $(VENV_DIR)/
	poetry install --no-root

build: pyproject.toml $(VENV_DIR)/
	poetry run python -m build $(BUILD_ARGS)

test: tests/
	poetry run pytest $(PYTEST_ARGS)

publish:
	poetry run twine upload -r pypi $(PROJECT_OUTDIR)/**

lint:
# stop the build if there are Python syntax errors or undefined names.
	poetry run flake8 . --count --statistics --extend-exclude=$(FLAKE8_EXCLUDE) --show-source --select=E9,F63,F7,F82
# --exit-zero treats all errors as warnings.
	poetry run flake8 . --count --statistics --extend-exclude=$(FLAKE8_EXCLUDE) --extend-ignore=W191,E251 --exit-zero --max-complexity=10 --max-line-length=$(MAX_LINE_LENGTH)

$(VENV_DIR):
	poetry run python -m venv ./$(VENV_DIR)
	poetry env use $(VENV_PYTHON)
