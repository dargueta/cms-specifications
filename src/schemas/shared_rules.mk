# SPDX-License-Identifier: BSD-3-Clause

%-min.json: %.json
	python3 -m scripts.minijson $< $@

$(TARGET_FORMAT_DIR)/%.yaml: $(TARGET_FORMAT_DIR)/%.json
	python3 -m scripts.json2yaml $< $@

$(TARGET_FORMAT_DIR)/%.json: $(CURDIR)/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml -I $(FORMATS_ROOT)/_common -o $@ --json $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

%: %.liquid
	python3 -m scripts.render_templates -I $(FORMATS_ROOT) -o $@ $^
