# SPDX-License-Identifier: BSD-3-Clause

BUILD_DIR=$(CURDIR)/build
PYTHONPATH:=$(CURDIR):$(PYTHONPATH)
export PYTHONPATH

.PHONY: all
all: beq4rx bqn4 fefd marxtr

.PHONY: clean
clean:
	$(RM) -r $(BUILD_DIR)
	find $(CURDIR) -depth -type d -empty -exec rmdir -v '{}' \+

%:
	$(MAKE) -C 'file_formats/$@' \
	    BUILD_ROOT='$(BUILD_DIR)' \
	    TARGET_FORMAT_DIR='$(BUILD_DIR)/$@' \
	    FORMATS_ROOT='$(CURDIR)/file_formats' \
	    all
