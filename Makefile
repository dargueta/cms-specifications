# SPDX-License-Identifier: BSD-3-Clause

VENV_DIR=$(CURDIR)/.venv
ACTIVATE_SCRIPT=$(VENV_DIR)/bin/activate
PYTHON_BIN=$(VENV_DIR)/bin/python3
ACTIVATE=source $(ACTIVATE_SCRIPT)
PYTHON=$(ACTIVATE) && python3
PIP=$(ACTIVATE) && pip
BUILD_SCRIPT=$(ACTIVATE) && doit

.PHONY: setup
setup: | $(PYTHON_BIN)


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

$(VENV_DIR):
	python3 -m venv $@

$(ACTIVATE_SCRIPT): | $(VENV_DIR)

$(PYTHON_BIN): | $(ACTIVATE_SCRIPT)
	$(PIP) install -Ur src/requirements.txt -r src/test-requirements.txt
