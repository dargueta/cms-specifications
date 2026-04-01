# SPDX-License-Identifier: BSD-3-Clause

.PHONY: schemas
schemas:
	$(MAKE) -C src/schemas BUILD_DIR='$(CURDIR)/build'


.PHONY: clean
clean:
	$(MAKE) -C src/schemas clean
	$(RM) -r build

.PHONY: format
format:
	ruff check --select I --fix
	ruff format

.PHONY: lint
lint:
	ruff check
