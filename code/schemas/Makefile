# SPDX-License-Identifier: BSD-3-Clause

.DELETE_ON_FAILURE: json/%.json dependencies.mk


YAML_SOURCES=$(shell find yaml -path '*/records/*.yml')
M4_YAML_SOURCES=$(shell find yaml -name '*.yml.m4')
M4_PUML_SOURCES=$(shell find yaml -name '*.puml.m4')
M4_DEPENDENCY_SPECS=$(M4_YAML_SOURCES:.m4=.dep) $(M4_PUML_SOURCES:.m4=.dep)
YAML_TARGETS=$(M4_YAML_SOURCES:.m4=)
PUML_TARGETS=$(M4_PUML_SOURCES:.m4=)
JSON_INTERMEDIATES=$(YAML_SOURCES:.yml=.json)
JSON_TARGETS=$(subst yaml/,json/,$(JSON_INTERMEDIATES))
JSON_TARGETS_MIN=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(YAML_TARGETS) $(PUML_TARGETS) $(JSON_TARGETS) $(JSON_TARGETS_MIN)


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

%.puml: %.puml.m4
	m4 -I yaml $< > $@

%.yml: %.yml.m4
	m4 -I yaml $< > $@

dependencies.mk: $(M4_DEPENDENCY_SPECS)
	cat $^ > $@

%.dep: %-debug-trace.txt
	echo -n "$*.yml: " > $@
	sed -E 's/^.* found `(.*)$$/\1/g' < $< | tr -d "'" >> $@

%-debug-trace.txt: %.m4
	m4 -I yaml --debug=p --debugfile=$@ $< >/dev/null

-include dependencies.mk
