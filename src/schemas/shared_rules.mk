# SPDX-License-Identifier: BSD-3-Clause

%-min.json: %.json
	python3 -m scripts.minijson $< $@

%.json: %.yaml
	python3 -m scripts.yaml2json $< $@

$(TARGET_FORMAT_DIR)/%.yaml: $(CURDIR)/%.yaml
	mkdir -p $(@D)
	python3 -m scripts.postprocess_yaml -I $(FORMATS_ROOT)/_common -o $@ $<
	check-jsonschema --schemafile $(TABLESCHEMA_URL) $@

$(TARGET_FORMAT_DIR)/%: $(CURDIR)/%
	mkdir -p $(@D)
	cp $< $@

$(CURDIR)/%: $(CURDIR)/%.liquid
	python3 -m scripts.render_templates -I $(FORMATS_ROOT) -o $@ $^
