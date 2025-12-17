# SPDX-License-Identifier: BSD-3-Clause
.DELETE_ON_FAILURE: json/%.json

YAML_SOURCES=$(shell find yaml -name '*.yml')
M4_SOURCES=$(shell find yaml -name '*.m4')
VALIDATION_INTERMEDIATES=$(YAML_SOURCES:.yml=-validation.json)
YAML_TARGETS=$(M4_SOURCES:.m4=.yml)
JSON_INTERMEDIATES=$(YAML_SOURCES:.yml=.json)
JSON_TARGETS=$(subst yaml/,json/,$(JSON_INTERMEDIATES))
JSON_TARGETS_MIN=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(JSON_TARGETS) $(JSON_TARGETS_MIN) $(YAML_TARGETS)


.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) $(ALL_TARGETS)

%-min.json: %.json
	yq -I0 -M -o json $< > $@

json/%.json: yaml/%.yml yaml/%-validation.json
	mkdir -p $(@D)
	yq -MP -o json $< > $@

%-validation.json: %.yml
	check-jsonschema -o $@ --schemafile https://datapackage.org/profiles/2.0/tableschema.json $<

%.yml: %.m4
	m4 -I yaml $< > $@
