GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS=records/detail.yaml records/header.yaml records/trailer.yaml record_layout.mmd
GENERIC_HEADER_DETAIL_TRAILER_VERSIONS=18.2 18.3 18.4 18.5 18.6 18.7 18.8 18.9
GENERIC_HEADER_DETAIL_TRAILER_TARGETS=$(foreach f,$(GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS),$(foreach v,$(GENERIC_HEADER_DETAIL_TRAILER_VERSIONS),$(v)/$(f)))

BEQ4RX_RENDERED_YAML_TARGETS=$(addprefix build/beq4rx/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
BQN4_RENDERED_YAML_TARGETS=$(addprefix build/bqn4/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
ALL_RENDERED_YAML_TARGETS=$(BEQ4RX_RENDERED_YAML_TARGETS) $(BQN4_RENDERED_YAML_TARGETS)

.DELETE_ON_FAILURE:

# TODO (dargueta): Consolidate these rules to avoid so much repetition?
# BEQ4RX -----------------------------------------------------------------------
build/beq4rx/18.8/%: build/beq4rx/18.9/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.7/%: build/beq4rx/18.8/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.6/%: build/beq4rx/18.7/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.5/%: build/beq4rx/18.6/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.4/%: build/beq4rx/18.5/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.3/%: build/beq4rx/18.4/%
	mkdir -p $(@D)
	ln -f $< $@
build/beq4rx/18.2/%: build/beq4rx/18.3/%
	mkdir -p $(@D)
	ln -f $< $@

# BQN4 -------------------------------------------------------------------------
build/bqn4/18.8/%: build/bqn4/18.9/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.7/%: build/bqn4/18.8/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.6/%: build/bqn4/18.7/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.5/%: build/bqn4/18.6/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.4/%: build/bqn4/18.5/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.3/%: build/bqn4/18.4/%
	mkdir -p $(@D)
	ln -f $< $@
build/bqn4/18.2/%: build/bqn4/18.3/%
	mkdir -p $(@D)
	ln -f $< $@
