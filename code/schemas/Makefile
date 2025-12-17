# SPDX-License-Identifier: BSD-3-Clause

.DELETE_ON_FAILURE: json/%.json dependencies.mk
.INTERMEDIATE: %.dep

YAML_SOURCES=$(shell find yaml -name '*.yml')
M4_SOURCES=$(shell find yaml -name '*.m4')
M4_DEPENDENCY_SPECS=$(M4_SOURCES:.m4=.dep)
YAML_TARGETS=$(M4_SOURCES:.m4=.yml)
JSON_INTERMEDIATES=$(YAML_SOURCES:.yml=.json)
JSON_TARGETS=$(subst yaml/,json/,$(JSON_INTERMEDIATES))
JSON_TARGETS_MIN=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(YAML_TARGETS) $(JSON_TARGETS) $(JSON_TARGETS_MIN)


.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) $(ALL_TARGETS) $(M4_DEPENDENCY_SPECS)

%-min.json: %.json
	yq -I0 -M -o json $< > $@

json/%.json: yaml/%.yml
	check-jsonschema --schemafile https://datapackage.org/profiles/2.0/tableschema.json $<
	mkdir -p $(@D)
	yq -MP -o json $< > $@

%.yml: %.m4
	m4 -I yaml --debug=p --debugfile=$<-trace.log $< > $@


M4_INCLUDE_OVERRIDE=m4_define(`include', `yaml/$$1')m4_dnl
export M4_INCLUDE_OVERRIDE

dependencies.mk: $(M4_DEPENDENCY_SPECS)
	cat $^ > $@

%.dep: %.m4
	echo "$*.yml: $< $(shell echo "$$M4_INCLUDE_OVERRIDE" | cat - $^ | m4 -P)" > $@

-include dependencies.mk
