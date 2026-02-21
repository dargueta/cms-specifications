GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS=records/detail.yaml records/header.yaml records/trailer.yaml parser-state-table.csv
GENERIC_HEADER_DETAIL_TRAILER_VERSIONS=18.6 18.7 18.8
GENERIC_HEADER_DETAIL_TRAILER_TARGETS=$(foreach f,$(GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS),$(foreach v,$(GENERIC_HEADER_DETAIL_TRAILER_VERSIONS),$(v)/$(f)))

BEQ4RX_RENDERED_YAML_TARGETS=$(addprefix build/beq4rx/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
BQN4_RENDERED_YAML_TARGETS=$(addprefix build/bqn4/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
ALL_RENDERED_YAML_TARGETS=$(BEQ4RX_RENDERED_YAML_TARGETS) $(BQN4_RENDERED_YAML_TARGETS)

.DELETE_ON_FAILURE:

# TODO (dargueta): Consolidate these rules to avoid so much repetition?
# BEQ4RX -----------------------------------------------------------------------
file_formats/beq4rx/18.9/%: file_formats/beq4rx/18.8/%
	mkdir -p $(@D)
	ln -f $< $@
file_formats/beq4rx/18.8/%: file_formats/beq4rx/18.7/%
	mkdir -p $(@D)
	ln -f $< $@
file_formats/beq4rx/18.7/%: file_formats/beq4rx/18.6/%
	mkdir -p $(@D)
	ln -f $< $@

# BQN4 -------------------------------------------------------------------------
file_formats/bqn4/18.9/%: file_formats/bqn4/18.8/%
	mkdir -p $(@D)
	ln -f $< $@
file_formats/bqn4/18.8/%: file_formats/bqn4/18.7/%
	mkdir -p $(@D)
	ln -f $< $@
file_formats/bqn4/18.7/%: file_formats/bqn4/18.6/%
	mkdir -p $(@D)
	ln -f $< $@
