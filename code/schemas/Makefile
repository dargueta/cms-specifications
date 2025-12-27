# SPDX-License-Identifier: BSD-3-Clause


YAML_SOURCES=$(shell find file_formats -name '*.yaml')
FSM_SOURCES=$(shell find file_formats -name 'parser-state-table.csv')
TEMPLATED_SOURCES=$(shell find file_formats -name '*.mako')
RENDERED_SOURCES=$(TEMPLATED_SOURCES:.mako=)

SIMPLE_TARGETS=$(subst file_formats/,build/,$(YAML_SOURCES) $(RENDERED_SOURCES))
YAML_TARGETS=$(filter %.yaml,$(SIMPLE_TARGETS))
PUML_TARGETS=$(foreach f,$(YAML_TARGETS),$(dir $f)../fsm.puml)
JSON_TARGETS=$(YAML_TARGETS:.yaml=.json)
JSON_MIN_TARGETS=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(YAML_TARGETS) $(PUML_TARGETS) $(JSON_TARGETS) $(JSON_MIN_TARGETS)

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json


.DELETE_ON_FAILURE:
# Uncomment this when debugging templates.
# .PRECIOUS: $(RENDERED_SOURCES)

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
	ln -f $< $@ || cp $< $@

build/%/fsm.puml: scripts/generate_plantuml.py \
                  file_formats/%/parser-state-table.csv
	mkdir -p $(@D)
	python3 $^ $@

build/%: file_formats/%
	mkdir -p $(@D)
	ln -f $< $@ || cp $< $@

file_formats/%: file_formats/%.mako
	python3 scripts/render_templates.py -I file_formats -o $@ $^

dependencies.mk: $(TEMPLATED_SOURCES)
	python3 scripts/render_templates.py -M -I file_formats -o $@ $^

-include dependencies.mk
