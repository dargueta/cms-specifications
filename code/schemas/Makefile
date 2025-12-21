# SPDX-License-Identifier: BSD-3-Clause

.DELETE_ON_FAILURE:

YAML_SOURCES=$(shell find file_formats -name '*.yaml')
PUML_SOURCES=$(shell find file_formats -name '*.puml')
TEMPLATED_SOURCES=$(shell find file_formats -name '*.m4')
RENDERED_SOURCES=$(TEMPLATED_SOURCES:.m4=)

SIMPLE_TARGETS=$(subst file_formats/,build/,$(YAML_SOURCES) $(PUML_SOURCES) $(RENDERED_SOURCES))
YAML_TARGETS=$(filter %.yaml,$(SIMPLE_TARGETS))
PUML_TARGETS=$(filter %.puml,$(SIMPLE_TARGETS))
JSON_TARGETS=$(YAML_TARGETS:.yaml=.json)
JSON_MIN_TARGETS=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(YAML_TARGETS) $(PUML_TARGETS) $(JSON_TARGETS) $(JSON_MIN_TARGETS)

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json


.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) -r build $(RENDERED_SOURCES)

%-min.json: %.json
	yq -I0 -M -o json $< > $@

%.json: %.yaml
	yq -MP -o json $< > $@

build/%.yaml: file_formats/%.yaml
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $<
	mkdir -p $(@D)
	cp $< $@

build/%: file_formats/%
	mkdir -p $(@D)
	cp $< $@

file_formats/%: file_formats/%.m4
	m4 -I file_formats $< > $@
