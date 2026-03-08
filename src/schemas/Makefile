# SPDX-License-Identifier: BSD-3-Clause

include dependencies.mk

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json

FINAL_JSON_TARGETS=$(ALL_RENDERED_TARGETS:.yaml=.json)
FINAL_MIN_JSON_TARGETS=$(FINAL_JSON_TARGETS:.json=-min.json)

ALL_TARGETS=$(ALL_RENDERED_TARGETS) $(FINAL_JSON_TARGETS) $(FINAL_MIN_JSON_TARGETS)


.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) -r build
	find $(CURDIR) -depth -type d -empty -exec rmdir -v '{}' \+

%-min.json: %.json
	python3 -m scripts.minijson $< $@

build/%.yaml: build/%.json
	python3 -m scripts.json2yaml $< $@

build/%.json: file_formats/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml -I file_formats/_common -o $@ --json $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

# *Never* symlink from `file_formats` into `build`! There's a race condition where,
# depending on the order Make picks, you could end up modifying original files.
# Always copy from `file_formats` into `build`, and link `build` to `build`.
build/%: file_formats/%
	mkdir -p $(@D)
	cp $< $@

file_formats/%: file_formats/%.liquid
	python3 -m scripts.render_templates -I file_formats -o $@ $^
