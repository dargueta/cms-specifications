// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  base: 'fefd/5.2/records/record.json',
  changes: [
    {
      selector: 'fields[name="race_code"]',
      new_value: pcug.race_code,
    },
  ],
}
