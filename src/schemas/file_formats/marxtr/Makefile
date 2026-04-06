include ../../functions.mk

RECORD_TYPES=header enrollment disenrollment


f_make_command=$(MAKE) \
    TARGET_FORMAT_DIR='$(TARGET_FORMAT_DIR)' \
    FILE_VERSION='$1' \
    $(addprefix $(TARGET_FORMAT_DIR)/$1/records/,$(foreach ext,.yaml .json -min.json,$(foreach stem,$(RECORD_TYPES),$(stem)$(ext)))) \
    '$(TARGET_FORMAT_DIR)/$1/record_layout.mmd'

.PHONY: all
all:
	$(call f_make_command,19.0)
	$(call f_make_command,18.9)

.INTERMEDIATE: $(CURDIR)/19.0/record_layout.mmd

$(CURDIR)/19.0/record_layout.mmd: $(CURDIR)/19.0/record_layout.mmd.liquid

$(TARGET_FORMAT_DIR)/$(FILE_VERSION)/%: $(TARGET_FORMAT_DIR)/19.0/%
	mkdir -p $(@D)
	ln -f $< $@

include ../../shared_rules.mk
