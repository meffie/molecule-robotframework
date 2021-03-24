# Copyright 2021 Sine Nomine Associates

.PHONY: help init lint test clean distclean

PYTHON3=python3
BIN=.venv/bin
PIP=$(BIN)/pip
YAMLLINT=$(BIN)/yamllint
ANSIBLE_LINT=$(BIN)/ansible-lint

DRIVER=docker
IMAGE=centos:8

help:
	@echo "usage: make <target>"
	@echo ""
	@echo "targets:"
	@echo "  init       create python virtual env"
	@echo "  lint       run linter"
	@echo "  test       run tests"
	@echo "  clean      remove generated files"
	@echo "  distclean  remove generated files and virtual env"

.venv:
	$(PYTHON3) -m venv .venv
	$(PIP) install -U pip
	$(PIP) install wheel
	$(PIP) install molecule[ansible,docker] molecule-virtup yamllint ansible-lint

init: .venv

lint: init
	$(YAMLLINT) tasks/*.yml tasks/pip/*.yml defaults/*.yml
	. $(BIN)/activate && $(ANSIBLE_LINT) .

check test: init lint
	. $(BIN)/activate && IMAGE=$(IMAGE) molecule test -d $(DRIVER)

clean:
	rm -rf .pytest_cache .cache .env.yml

distclean: clean
	rm -rf .venv
