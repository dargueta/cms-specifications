include ../../functions.mk

.PHONY: all
all:
	$(call f_default_header_detail_trailer_command,5,0)
	$(call f_default_header_detail_trailer_command,5,1)
	$(call f_default_header_detail_trailer_command,5,2)
	$(call f_default_header_detail_trailer_command,5,3)
	$(call f_default_header_detail_trailer_command,6,0)
	$(call f_default_header_detail_trailer_command,6,1)
	$(call f_default_header_detail_trailer_command,6,2)
	$(call f_default_header_detail_trailer_command,6,3)
	$(call f_default_header_detail_trailer_command,7,0)
	$(call f_default_header_detail_trailer_command,7,1)
	$(call f_default_header_detail_trailer_command,7,2)
	# v7.3 does not appear to exist.
	$(call f_default_header_detail_trailer_command,8,0)
	$(call f_default_header_detail_trailer_command,8,1)
	$(call f_default_header_detail_trailer_command,8,2)
	$(call f_default_header_detail_trailer_command,8,3)
	$(call f_default_header_detail_trailer_command,9,0)
	$(call f_default_header_detail_trailer_command,9,1)
	$(call f_default_header_detail_trailer_command,9,2)
	$(call f_default_header_detail_trailer_command,9,3)
	$(call f_default_header_detail_trailer_command,10,0)
	$(call f_default_header_detail_trailer_command,10,1)
	$(call f_default_header_detail_trailer_command,10,2)
	$(call f_default_header_detail_trailer_command,10,3)
	$(call f_default_header_detail_trailer_command,11,0)
	$(call f_default_header_detail_trailer_command,11,1)
	$(call f_default_header_detail_trailer_command,11,2)
	$(call f_default_header_detail_trailer_command,11,3)
	$(call f_default_header_detail_trailer_command,12,0)
	$(call f_default_header_detail_trailer_command,12,1)
	$(call f_default_header_detail_trailer_command,12,2)
	$(call f_default_header_detail_trailer_command,12,3)
	$(call f_default_header_detail_trailer_command,13,0)
	$(call f_default_header_detail_trailer_command,13,1)
	$(call f_default_header_detail_trailer_command,13,2)
	$(call f_default_header_detail_trailer_command,13,3)
	$(call f_default_header_detail_trailer_command,14,0)
	$(call f_default_header_detail_trailer_command,14,1)
	$(call f_default_header_detail_trailer_command,14,2)
	$(call f_default_header_detail_trailer_command,14,3)
	$(call f_default_header_detail_trailer_command,15,0)
	$(call f_default_header_detail_trailer_command,15,1)
	$(call f_default_header_detail_trailer_command,15,2)
	$(call f_default_header_detail_trailer_command,15,3)
	$(call f_default_header_detail_trailer_command,15,4)
	$(call f_default_header_detail_trailer_command,16,0)
	$(call f_default_header_detail_trailer_command,16,1)
	$(call f_default_header_detail_trailer_command,16,2)
	$(call f_default_header_detail_trailer_command,16,3)
	$(call f_default_header_detail_trailer_command,16,4)
	$(call f_default_header_detail_trailer_command,17,1)
	$(call f_default_header_detail_trailer_command,17,2)
	$(call f_default_header_detail_trailer_command,17,3)
	$(call f_default_header_detail_trailer_command,17,4)
	$(call f_default_header_detail_trailer_command,17,5)
	$(call f_default_header_detail_trailer_command,17,6)
	$(call f_default_header_detail_trailer_command,17,7)
	$(call f_default_header_detail_trailer_command,17,8)
	$(call f_default_header_detail_trailer_command,17,9)
	$(call f_default_header_detail_trailer_command,18,0)
	$(call f_default_header_detail_trailer_command,18,1)
	$(call f_default_header_detail_trailer_command,18,2)
	$(call f_default_header_detail_trailer_command,18,3)
	$(call f_default_header_detail_trailer_command,18,4)
	$(call f_default_header_detail_trailer_command,18,5)
	$(call f_default_header_detail_trailer_command,18,6)
	$(call f_default_header_detail_trailer_command,18,7)
	$(call f_default_header_detail_trailer_command,18,8)
	$(call f_default_header_detail_trailer_command,18,9)
	$(call f_default_header_detail_trailer_command,19,0)

$(TARGET_FORMAT_DIR)/5.0/record_layout.mmd: $(CURDIR)/README.md
	python3 -m scripts.mermaid_from_markdown $< $@

$(TARGET_FORMAT_DIR)/$(FILE_VERSION)/record_layout.mmd: $(TARGET_FORMAT_DIR)/5.0/record_layout.mmd
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/5.1/records/header%: $(TARGET_FORMAT_DIR)/5.0/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/5.1/records/trailer%: $(TARGET_FORMAT_DIR)/5.0/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/5.2/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/5.3/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/6.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/7.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/8.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/9.0/%: $(TARGET_FORMAT_DIR)/5.1/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/9.1/records/header%: $(TARGET_FORMAT_DIR)/5.1/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/9.1/records/trailer%: $(TARGET_FORMAT_DIR)/5.1/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/9.3/%: $(TARGET_FORMAT_DIR)/9.2/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/10.0/records/header%: $(TARGET_FORMAT_DIR)/9.2/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/10.0/records/trailer%: $(TARGET_FORMAT_DIR)/9.2/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/10.1/%: $(TARGET_FORMAT_DIR)/10.0/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/10.2/%: $(TARGET_FORMAT_DIR)/10.0/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/11.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/10.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.0/records/header%: $(TARGET_FORMAT_DIR)/10.3/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.0/records/trailer%: $(TARGET_FORMAT_DIR)/10.3/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.1/%: $(TARGET_FORMAT_DIR)/12.0/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.2/%: $(TARGET_FORMAT_DIR)/12.0/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.3/records/header%: $(TARGET_FORMAT_DIR)/12.0/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/12.3/records/trailer%: $(TARGET_FORMAT_DIR)/12.0/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/13.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/12.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/14.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/12.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.0/%: $(TARGET_FORMAT_DIR)/12.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.1/%: $(TARGET_FORMAT_DIR)/12.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.2/%: $(TARGET_FORMAT_DIR)/12.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.3/records/header%: $(TARGET_FORMAT_DIR)/12.3/records/header%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.3/records/trailer%: $(TARGET_FORMAT_DIR)/12.3/records/trailer%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/15.4/%: $(TARGET_FORMAT_DIR)/15.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/16.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/15.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/17.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/15.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/18.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/15.3/%
	mkdir -p $(@D)
	ln -f $< $@

$(TARGET_FORMAT_DIR)/19.$(FILE_VERSION_MINOR)/%: $(TARGET_FORMAT_DIR)/15.3/%
	mkdir -p $(@D)
	ln -f $< $@

include ../../shared_rules.mk
