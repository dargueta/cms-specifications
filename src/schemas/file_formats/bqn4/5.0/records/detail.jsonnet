// SPDX-License-Identifier: BSD-3-Clause

local base_detail_record = import 'bqn4/common/detail.jsonnet';
local filler = import 'filler.jsonnet';

base_detail_record {
  fields+: [
    filler('record_padding', 118),
  ],
}
