// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/records/data/5.0.jsonnet';
local pcug = import 'pcug.libjsonnet';

base {
  __patch__+: [
    {
      selector: '$.fields[?(@.name == "premium_withhold_option_parts_c_d")]',
      new_value: pcug.filler('premium_withhold_option_parts_c_d', 1),
    },
  ],
}
