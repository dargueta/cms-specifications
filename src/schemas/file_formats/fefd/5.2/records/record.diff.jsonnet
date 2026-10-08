// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/5.0/records/record.jsonnet';
local filler = import 'filler.jsonnet';

base {
  __changes__: {
    premium_withhold_option_parts_c_d: filler('premium_withhold_option_parts_c_d', 1),
  },
}
