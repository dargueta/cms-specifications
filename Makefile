# SPDX-License-Identifier: BSD-3-Clause

.PHONY: schemas
schemas:
	cd src && doit


.PHONY: clean
clean:
	doit clean -f src/dodo.py -a
	$(RM) -r build

.PHONY: format
format:
	ruff check --select I --fix src tests
	ruff format src tests

.PHONY: lint
lint:
	ruff check src tests

.PHONY: typing
typing:
	pyrefly check


.PHONY: setup
setup:
	pip3 install -r dev-requirements.txt
	$(MAKE) pin


#---------------------------------------------------------------------------------------
# Handle dependencies
.PHONY: pin
pin: dev-requirements.txt test-requirements.txt requirements.txt
	pip-sync $^

requirements.txt: requirements.in .pip-tools.toml
	pip-compile -v -o $@ $<

test-requirements.txt: test-requirements.in requirements.txt .pip-tools.toml
	pip-compile -v -o $@ $<

dev-requirements.txt: dev-requirements.in requirements.txt test-requirements.txt .pip-tools.toml
	pip-compile -v -o $@ $<
