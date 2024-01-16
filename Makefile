# Copyright 2020-2021 Sine Nomine Associates
#
# This is a helper makefile to run tox. Run tox directly if make is not
# available:
#
#    $ python3 -m venv .venv
#    $ source .venv/bin/activate
#    (venv) $ pip install -U pip setuptools
#    (venv) $ pip install tox
#    (venv) $ tox
#

PYTHON3=python3
PIP=.venv/bin/pip
TOX=.venv/bin/tox

.PHONY: help
help:
	@echo "usage: make <target>"
	@echo ""
	@echo "targets:"
	@echo "  init       create python venv to run tox"
	@echo "  lint       run lint checks"
	@echo "  check      run quick tests"
	@echo "  test       run all tests"
	@echo "  docs       generate html docs"
	@echo "  preview    local preview html docs"
	@echo "  release    upload to pypi.org"
	@echo "  clean      remove generated files"
	@echo "  distclean  remove generated files and venvs"

.venv/bin/activate: Makefile
	$(PYTHON3) -m venv .venv
	$(PIP) install -U pip
	$(PIP) install tox
	touch .venv/bin/activate

.PHONY: init
init: .venv/bin/activate

.PHONY: lint
lint: init
	$(TOX) -e lint

.PHONY: check
check: lint
	$(TOX) -e py312-mol603 -- -k 'not vagrant'

.PHONY: test
test: lint
	$(TOX)

.PHONY: docs
docs: init
	$(TOX) -e docs

.PHONY: preview
preview: docs
	xdg-open docs/build/html/index.html

.PHONY: release upload
release upload: init
	$(TOX) -e release

.PHONY: clean
clean:
	rm -rf .pytest_cache src/*/__pycache__ tests/__pycache__
	rm -rf tests/molecule/*/output
	rm -rf build dist
	rm -rf .eggs *.egg-info src/*.egg-info
	rm -rf docs/build

.PHONY: reallyclean distclean
reallyclean distclean: clean
	rm -rf .config .venv .tox
