// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/5.2/records/record.jsonnet';
local race_code = import 'race_code.jsonnet';

base {
  __changes__: {
    race_code: race_code,
  },
}
