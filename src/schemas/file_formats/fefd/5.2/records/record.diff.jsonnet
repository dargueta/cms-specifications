// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  base: '5.0/records/record.json',
  changes: [
    {
      selector: '$.fields[?(@.name == "premium_withhold_option_parts_c_d")]',
      new_value: pcug.filler('premium_withhold_option_parts_c_d', 1),
    },
  ],
}
