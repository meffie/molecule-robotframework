# Copyright 2021 Sine Nomine Associates

.PHONY: help init lint test clean distclean

PYTHON3=python3
BIN=.venv/bin
PIP=$(BIN)/pip
YAMLLINT=$(BIN)/yamllint
ANSIBLE_LINT=$(BIN)/ansible-lint

help:
	@echo "usage: make <target>"
	@echo ""
	@echo "targets:"
	@echo "  init       create python virtual env"
	@echo "  lint       run linter"
	@echo "  test       run tests (requires docker)"
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
	. $(BIN)/activate && IMAGE=centos:8 molecule test
	. $(BIN)/activate && IMAGE=centos:7 molecule test
	. $(BIN)/activate && IMAGE=fedora:34 molecule test
	. $(BIN)/activate && IMAGE=fedora:33 molecule test
	. $(BIN)/activate && IMAGE=debian:11 molecule test
	. $(BIN)/activate && IMAGE=debian:10 molecule test

clean:
	rm -rf .pytest_cache .cache .env.yml

distclean: clean
	rm -rf .venv
