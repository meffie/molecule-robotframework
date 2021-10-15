# Copyright 2020-2021 Sine Nomine Associates

.PHONY: help init lint import test docs sdist wheel rpm deb upload clean distclean

ROLE_VERSION=1.2.0
PYTHON3=python3
BIN=.venv/bin
PIP=$(BIN)/pip
PYTHON=$(BIN)/python
PYFLAKES=$(BIN)/pyflakes
YAMLLINT=$(BIN)/yamllint
PYTEST=$(BIN)/pytest
TWINE=$(BIN)/twine

help:
	@echo "usage: make <target>"
	@echo ""
	@echo "targets:"
	@echo "  init       create python virtual env"
	@echo "  lint       run linter"
	@echo "  import     import external ansible roles"
	@echo "  test       run tests"
	@echo "  docs       build html docs"
	@echo "  sdist      create source distribution"
	@echo "  wheel      create wheel distribution"
	@echo "  rpm        create rpm package"
	@echo "  deb        create deb package"
	@echo "  upload     upload to pypi.org"
	@echo "  clean      remove generated files"
	@echo "  distclean  remove generated files and virtual env"

.venv:
	$(PYTHON3) -m venv .venv
	$(PIP) install -U pip
	$(PIP) install wheel
	$(PIP) install pyflakes pylint yamllint pytest collective.checkdocs twine
	$(PIP) install sphinx sphinx-rtd-theme
	$(PIP) install molecule[ansible] molecule-docker molecule-vagrant molecule-virtup python-vagrant
	$(PIP) install -e .

init: .venv

lint: init
	$(PYFLAKES) src/*/*.py
	$(PYFLAKES) tests/*.py
	$(YAMLLINT) src/*/playbooks/*.yml
	$(YAMLLINT) tests/scenarios/*/molecule/default/*.yml
	$(PYTHON) setup.py -q checkdocs

import:
	mkdir -p src/molecule_robotframework/playbooks/roles/robotframework
	git clone https://github.com/meffie/ansible-role-robotframework.git /tmp/ansible-role-robotframework.git
	(cd /tmp/ansible-role-robotframework.git && git archive $(ROLE_VERSION)) | \
	  (cd src/molecule_robotframework/playbooks/roles/robotframework && tar xf -)
	rm -rf src/molecule_robotframework/playbooks/roles/robotframework/molecule
	rm -rf /tmp/ansible-role-robotframework.git

check test: init lint
	. .venv/bin/activate && pytest -v $(T) tests

doc docs:
	$(MAKE) -C docs html

sdist: init
	$(PYTHON) setup.py sdist

wheel: init
	$(PYTHON) setup.py bdist_wheel

rpm: init
	$(PYTHON) setup.py bdist_rpm

deb: init
	$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb

upload: init sdist wheel
	$(TWINE) upload dist/*

clean:
	rm -rf .pytest_cache
	rm -rf src/*/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/scenarios/*/*/molecule/default/library/__pycache__/
	rm -rf build dist
	rm -rf .eggs *.egg-info src/*.egg-info
	rm -rf docs/build

distclean: clean
	rm -rf .venv
