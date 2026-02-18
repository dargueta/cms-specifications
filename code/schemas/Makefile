# SPDX-License-Identifier: BSD-3-Clause

FILE_FORMAT_DIRS=$(filter-out %/_common,$(wildcard file_formats/*))
ALL_FILE_VERSION_DIRS=$(foreach f,$(FILE_FORMAT_DIRS),$(wildcard $(f)/*))
RECORD_DEF_SOURCES=$(foreach v,$(ALL_FILE_VERSION_DIRS),$(wildcard $(v)/records/*.yaml))
TEMPLATE_RECORD_DEF_SOURCES=$(foreach v,$(ALL_FILE_VERSION_DIRS),$(wildcard $(v)/records/*.yaml.mako))
LAYOUT_SOURCES=$(foreach v,$(ALL_FILE_VERSION_DIRS),$(wildcard $(v)/parser-state-table.csv))
TEMPLATE_LAYOUT_SOURCES=$(foreach v,$(ALL_FILE_VERSION_DIRS),$(wildcard $(v)/parser-state-table.csv.mako))

ALL_TEMPLATED_SOURCES=$(TEMPLATE_RECORD_DEF_SOURCES) $(TEMPLATE_LAYOUT_SOURCES)
ALL_RENDERED_SOURCES=$(ALL_TEMPLATED_SOURCES:.mako=)

SIMPLE_TARGETS=$(subst file_formats/,build/,$(RECORD_DEF_SOURCES) $(LAYOUT_SOURCES) $(ALL_RENDERED_SOURCES))
YAML_TARGETS=$(filter %.yaml,$(SIMPLE_TARGETS))
PUML_TARGETS=$(foreach f,$(YAML_TARGETS),$(dir $f)../fsm.puml)
JSON_TARGETS=$(YAML_TARGETS:.yaml=.json)
JSON_MIN_TARGETS=$(JSON_TARGETS:.json=-min.json)
ALL_TARGETS=$(YAML_TARGETS) $(PUML_TARGETS) $(JSON_TARGETS) $(JSON_MIN_TARGETS)

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json


.DELETE_ON_FAILURE:
# Uncomment this when debugging templates.
# .PRECIOUS: $(ALL_RENDERED_SOURCES)

.PHONY: all
all: $(ALL_TARGETS)

.PHONY: clean
clean:
	$(RM) -r build $(ALL_RENDERED_SOURCES)

.PHONY: show-vars
show-vars:
	@echo "FILE FORMAT DIRS ---------------------------------------------------"
	@echo $(FILE_FORMAT_DIRS)
	@echo
	@echo "RECORD FILES -------------------------------------------------------"
	@echo $(RECORD_DEF_SOURCES)
	@echo
	@echo "TEMPLATE RECORD FILES ----------------------------------------------"
	@echo $(TEMPLATE_RECORD_DEF_SOURCES)
	@echo
	@echo "LAYOUT FILES -------------------------------------------------------"
	@echo $(LAYOUT_SOURCES)
	@echo
	@echo "TEMPLATE LAYOUT FILES ----------------------------------------------"
	@echo $(TEMPLATE_LAYOUT_SOURCES)
	@echo
	@echo "RENDERED SOURCES ---------------------------------------------------"
	@echo $(ALL_RENDERED_SOURCES)
	@echo
	@echo "ALL TARGETS --------------------------------------------------------"
	@echo $(ALL_TARGETS)

%-min.json: %.json
	python3 -m scripts.minijson $< $@

build/%.yaml: build/%.json
	python3 -m scripts.json2yaml $< $@

build/%.json: file_formats/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml -I file_formats/_common -o $@ --json $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

build/%/fsm.puml: scripts/generate_plantuml.py \
                  file_formats/%/parser-state-table.csv
	mkdir -p $(@D)
	python3 $^ $@

build/%: file_formats/%
	mkdir -p $(@D)
	ln -f $< $@ || cp $< $@

file_formats/%: file_formats/%.mako
	python3 -m scripts.render_templates -I file_formats -o $@ $^

dependencies.mk: $(ALL_TEMPLATED_SOURCES)
	python3 -m scripts.render_templates -M -I file_formats -o $@ $^

-include dependencies.mk
