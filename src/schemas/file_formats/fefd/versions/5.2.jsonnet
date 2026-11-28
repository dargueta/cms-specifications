// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/versions/5.0.jsonnet';
local pcug = import 'pcug.libjsonnet';

base {
  __patch__+: [
    {
      selector: '$.version',
      new_value: '5.2',
    },
    {
      selector: '$.schema[0].properties[?(@.physicalName == "premium_withhold_option_parts_c_d")]',
      new_value: pcug.filler('premium_withhold_option_parts_c_d', 1),
    },
  ],
}
