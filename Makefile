# SPDX-License-Identifier: BSD-3-Clause

VENV_DIR=$(CURDIR)/.venv
ACTIVATE=$(VENV_DIR)/bin/activate
PYTHON_BIN=$(VENV_DIR)/bin/python3
PYTHON=source $(ACTIVATE) && python3
PIP=source $(ACTIVATE) && pip
RUN_BUILD_SCRIPT=pymake

.PHONY: setup
setup: | $(PYTHON_BIN)


.PHONY: schemas
schemas: | $(PYTHON_BIN)
	pymake run src/schemas


.PHONY: clean
clean: | $(PYTHON_BIN)
	cd src && (BUILD_SCRIPT) clean
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

$(ACTIVATE): | $(VENV_DIR)

$(PYTHON_BIN): | $(ACTIVATE)
	$(PIP) install -Ur src/requirements.txt -r src/test-requirements.txt
