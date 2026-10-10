// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/5.2/records/record.jsonnet';
local pcug = import 'pcug.libjsonnet';

base {
  __changes__: {
    race_code: pcug.race_code,
  },
}
