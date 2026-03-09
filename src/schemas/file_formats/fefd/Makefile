include ../../functions.mk

.PHONY: all
all:
	$(call f_default_single_record_command,19.0)
	$(call f_default_single_record_command,18.9)
	$(call f_default_single_record_command,18.8)
	$(call f_default_single_record_command,18.7)
	$(call f_default_single_record_command,18.6)
	$(call f_default_single_record_command,18.5)
	$(call f_default_single_record_command,18.4)
	$(call f_default_single_record_command,18.3)
	$(call f_default_single_record_command,18.2)
	$(call f_default_single_record_command,18.1)
	$(call f_default_single_record_command,18.0)
	$(call f_default_single_record_command,17.9)
	$(call f_default_single_record_command,17.8)
	$(call f_default_single_record_command,17.7)
	$(call f_default_single_record_command,17.6)
	$(call f_default_single_record_command,17.5)
	$(call f_default_single_record_command,17.4)
	$(call f_default_single_record_command,17.3)
	$(call f_default_single_record_command,17.2)
	$(call f_default_single_record_command,17.1)
	$(call f_default_single_record_command,16.4)
	$(call f_default_single_record_command,16.3)
	$(call f_default_single_record_command,16.2)
	$(call f_default_single_record_command,16.1)
	$(call f_default_single_record_command,16.0)
	$(call f_default_single_record_command,15.4)
	$(call f_default_single_record_command,15.3)

$(TARGET_FORMAT_DIR)/$(FILE_VERSION)/%: $(TARGET_FORMAT_DIR)/19.0/%
	mkdir -p $(@D)
	ln -f $< $@

include ../../shared_rules.mk
