// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/versions/5.2.jsonnet';
local pcug = import 'pcug.libjsonnet';

base {
  __patch__+: [
    {
      selector: '$.version',
      new_value: '14.3',
    },
    {
      selector: '$.schema[0].properties[?(@.physicalName == "race_code")]',
      new_value: pcug.race_code,
    },
  ],
}
