# SPDX-License-Identifier: BSD-3-Clause

%-min.json: %.json
	python3 -m scripts.minijson $< $@

$(TARGET_FORMAT_DIR)/%.yaml: $(TARGET_FORMAT_DIR)/%.json
	python3 -m ruamel.yaml.cmd from-json $< > $@

$(TARGET_FORMAT_DIR)/%.json: $(CURDIR)/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml --json -I $(FORMATS_ROOT)/_common -o $@ $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

$(TARGET_FORMAT_DIR)/%: $(CURDIR)/%
	mkdir -p $(@D)
	cp $< $@

# File layouts are usually fairly stable, and it's helpful for the user to see
# at a glance how a file is laid out, so by default we store the record layout
# in the file format's README.
#
# Files that have had layout changes over time will need to define
# record_layout.mmd in place and override this rule. Unfortunately, that forces
# them to include this file relatively early, but that should be fine.
# $(TARGET_FORMAT_DIR)%/record_layout.mmd: $(CURDIR)/README.md
# 	python3 -m scripts.mermaid_from_markdown $< $@

$(CURDIR)/%: $(CURDIR)/%.liquid
	python3 -m scripts.render_templates -I $(FORMATS_ROOT) -o $@ $^
