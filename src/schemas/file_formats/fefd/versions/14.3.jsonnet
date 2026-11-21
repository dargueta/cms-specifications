// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/records/data/5.2.jsonnet';
local pcug = import 'pcug.libjsonnet';

base {
  __patch__+: [
    {
      selector: '$.fields[?(@.name == "race_code")]',
      new_value: pcug.race_code,
    },
  ],
}
