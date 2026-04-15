# SPDX-License-Identifier: BSD-3-Clause

.INTERMEDIATE: $(CURDIR)/record_layout.mmd

%-min.json: %.json
	python3 -m scripts.minijson $< $@

$(TARGET_FORMAT_DIR)/%.yaml: $(TARGET_FORMAT_DIR)/%.json
	python3 -m ruamel.yaml.cmd from-json $< > $@

$(TARGET_FORMAT_DIR)/%.json: $(CURDIR)/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml --json -I $(FORMATS_ROOT)/_common -o $@ $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

$(TARGET_FORMAT_DIR)/%/record_layout.mmd: $(CURDIR)/record_layout.mmd
	mkdir -p $(@D)
	ln -f $< $@

$(CURDIR)/record_layout.mmd: $(CURDIR)/README.md
	awk '/^```mermaid$$/{f=1;next} f&&/^```$$/{exit} f' $< > $@

$(TARGET_FORMAT_DIR)/%: $(CURDIR)/%
	mkdir -p $(@D)
	cp $< $@

$(CURDIR)/%: $(CURDIR)/%.liquid
	python3 -m scripts.render_templates -I $(FORMATS_ROOT) -o $@ $^
