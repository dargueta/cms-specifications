# SPDX-License-Identifier: BSD-3-Clause

include dependencies.mk

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json

FINAL_JSON_TARGETS=$(ALL_RENDERED_YAML_TARGETS:.yaml=.json)
FINAL_MIN_JSON_TARGETS=$(FINAL_JSON_TARGETS:.json=-min.json)

ALL_TARGETS=$(ALL_RENDERED_YAML_TARGETS) $(FINAL_JSON_TARGETS) $(FINAL_MIN_JSON_TARGETS)


.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) -r build

%-min.json: %.json
	python3 -m scripts.minijson $< $@

build/%.yaml: build/%.json
	python3 -m scripts.json2yaml $< $@

build/%.json: file_formats/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml -I file_formats/_common -o $@ --json $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

build/%/fsm.puml: build/%/parser-state-table.csv
	mkdir -p $(@D)
	python3 -m scripts/generate_plantuml $^ $@

build/%: file_formats/%
	mkdir -p $(@D)
	ln $< $@ || cp $< $@

file_formats/%: file_formats/%.liquid
	python3 -m scripts.render_templates -I file_formats -o $@ $^
