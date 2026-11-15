// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/12.0/records/detail.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    pcug.date8 {
      name: 'most_recent_duals_sep_use_date',
      title: 'Most Recent Duals SEP Use Date',
    },
  ] + std.flattenArrays([
    [
      pcug.date8 {
        name: 'cara_status_start_date_%d' % i,
        title: 'CARA Status Start Date (%d)' % i,
      },
      pcug.date8 {
        name: 'cara_status_end_date_%d' % i,
        title: 'CARA Status End Date (%d)' % i,
      },
    ]
    for i in std.range(1, 10)
  ]),
  padding_length:: 266,
}
