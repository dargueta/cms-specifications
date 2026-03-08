GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS=records/detail.yaml records/header.yaml records/trailer.yaml record_layout.mmd
GENERIC_HEADER_DETAIL_TRAILER_TARGETS=$(foreach f,$(GENERIC_HEADER_DETAIL_TRAILER_FILE_COMPONENTS),$(foreach v,$(GENERIC_SUPPORTED_VERSIONS),$(v)/$(f)))
GENERIC_SUPPORTED_VERSIONS=\
    15.3 15.4 \
    16.0 16.1 16.2 16.3 16.4 \
    17.1 17.2 17.3 17.4 17.5 17.6 17.7 17.8 17.9 \
    18.0 18.1 18.2 18.3 18.4 18.5 18.6 18.7 18.8 18.9 \
    19.0

BEQ4RX_RENDERED_TARGETS=$(addprefix build/beq4rx/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
BQN4_RENDERED_TARGETS=$(addprefix build/bqn4/,$(GENERIC_HEADER_DETAIL_TRAILER_TARGETS))
FEFD_RENDERED_TARGETS=$(foreach v,$(GENERIC_SUPPORTED_VERSIONS),build/fefd/$v/records/record.yaml) \
    $(foreach v,$(GENERIC_SUPPORTED_VERSIONS),build/fefd/$v/record_layout.mmd)
MARXTR_RENDERED_TARGETS=build/marxtr/18.9/record_layout.mmd
ALL_RENDERED_TARGETS=\
    $(BEQ4RX_RENDERED_TARGETS) \
    $(BQN4_RENDERED_TARGETS) \
    $(MARXTR_RENDERED_TARGETS) \
    $(FEFD_RENDERED_TARGETS)

.DELETE_ON_FAILURE:

# TODO (dargueta): Consolidate these rules to avoid so much repetition?
# BEQ4RX -----------------------------------------------------------------------
build/beq4rx/18.9/%: build/beq4rx/19.0/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.8/%: build/beq4rx/18.9/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.7/%: build/beq4rx/18.8/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.6/%: build/beq4rx/18.7/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.5/%: build/beq4rx/18.6/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.4/%: build/beq4rx/18.5/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.3/%: build/beq4rx/18.4/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.2/%: build/beq4rx/18.3/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.1/%: build/beq4rx/18.2/%
	mkdir -p $(@D) && ln -f $< $@
build/beq4rx/18.0/%: build/beq4rx/18.1/%
	mkdir -p $(@D) && ln -f $< $@

# BQN4 -------------------------------------------------------------------------
build/bqn4/18.9/%: build/bqn4/19.0/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.8/%: build/bqn4/18.9/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.7/%: build/bqn4/18.8/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.6/%: build/bqn4/18.7/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.5/%: build/bqn4/18.6/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.4/%: build/bqn4/18.5/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.3/%: build/bqn4/18.4/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.2/%: build/bqn4/18.3/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.1/%: build/bqn4/18.2/%
	mkdir -p $(@D) && ln -f $< $@
build/bqn4/18.0/%: build/bqn4/18.1/%
	mkdir -p $(@D) && ln -f $< $@

# FEFD -----------------------------------------------------------------------
build/fefd/18.9/%: build/fefd/19.0/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.8/%: build/fefd/18.9/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.7/%: build/fefd/18.8/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.6/%: build/fefd/18.7/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.5/%: build/fefd/18.6/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.4/%: build/fefd/18.5/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.3/%: build/fefd/18.4/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.2/%: build/fefd/18.3/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.1/%: build/fefd/18.2/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/18.0/%: build/fefd/18.1/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/17.9/%: build/fefd/18.0/%
	mkdir -p $(@D) && ln -f $< $@
build/fefd/17.8/%: build/fefd/17.9/%
	mkdir -p $(@D) && ln -f $< $@
