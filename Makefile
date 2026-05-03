# SPDX-License-Identifier: BSD-3-Clause

VENV_DIR=$(CURDIR)/.venv
ACTIVATE_SCRIPT=$(VENV_DIR)/bin/activate
PYTHON_BIN=$(VENV_DIR)/bin/python3
ACTIVATE=source $(ACTIVATE_SCRIPT)
PYTHON=$(ACTIVATE) && python3
PIP=$(PYTHON) -m pip
PIP_COMPILE=$(ACTIVATE) && pip-compile
PIP_SYNC=$(ACTIVATE) && pip-sync
BUILD_SCRIPT=$(ACTIVATE) && doit

.PHONY: setup
setup: dev-requirements.txt test-requirements.txt requirements.txt | $(ACTIVATE_SCRIPT)
	$(PIP) install -r $<
	$(PIP_SYNC) $^


.PHONY: schemas
schemas: | $(PYTHON_BIN)
	cd src && $(BUILD_SCRIPT) run


.PHONY: clean
clean: | $(PYTHON_BIN)
	cd src && $(BUILD_SCRIPT) clean
	$(RM) -r build

.PHONY: format
format:
	ruff check --select I --fix src Makefile.py
	ruff format src Makefile.py

.PHONY: lint
lint:
	ruff check src Makefile.py

.PHONY: typing
typing:
	pyrefly check

$(VENV_DIR):
	python3 -m venv $@

$(ACTIVATE_SCRIPT): | $(VENV_DIR)

#---------------------------------------------------------------------------------------
# Handle dependencies
requirements.txt: requirements.in .pip-tools.toml
	$(PIP_COMPILE) -v -o $@ $<

test-requirements.txt: test-requirements.in requirements.txt .pip-tools.toml
	$(PIP_COMPILE) -v -o $@ $<

dev-requirements.txt: dev-requirements.in requirements.txt test-requirements.txt .pip-tools.toml
	$(PIP_COMPILE) -v -o $@ $<
