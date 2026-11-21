// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/common/records/detail/12.0.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    pcug.date8 {
      name: 'Most Recent Duals SEP Use Date',
      physicalName: 'most_recent_duals_sep_use_date',
    },
  ] + std.flattenArrays([
    [
      pcug.date8 {
        name: 'CARA Status Start Date (%d)' % i,
        physicalName: 'cara_status_start_date_%d' % i,
      },
      pcug.date8 {
        name: 'CARA Status End Date (%d)' % i,
        physicalName: 'cara_status_end_date_%d' % i,
      },
    ]
    for i in std.range(1, 10)
  ]),
  padding_length:: 266,
}
