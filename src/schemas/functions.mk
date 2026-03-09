# SPDX-License-Identifier: BSD-3-Clause

TABLESCHEMA_URL=https://datapackage.org/profiles/2.0/tableschema.json

f_default_header_detail_trailer_command=$(MAKE) \
    TARGET_FORMAT_DIR='$(TARGET_FORMAT_DIR)' \
    FILE_VERSION='$1' \
    $(addprefix $(TARGET_FORMAT_DIR)/$1/records/,$(foreach ext,.yaml .json -min.json,$(foreach stem,header detail trailer,$(stem)$(ext)))) \
    '$(TARGET_FORMAT_DIR)/$1/record_layout.mmd'


f_default_single_record_command=$(MAKE) \
    TARGET_FORMAT_DIR='$(TARGET_FORMAT_DIR)' \
    FILE_VERSION='$1' \
    '$(TARGET_FORMAT_DIR)/$1/records/record.yaml' \
    '$(TARGET_FORMAT_DIR)/$1/records/record.json' \
    '$(TARGET_FORMAT_DIR)/$1/records/record-min.json' \
    '$(TARGET_FORMAT_DIR)/$1/record_layout.mmd'
