// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/12.0/records/detail.jsonnet';
local date8 = import 'date8.jsonnet';


base {
  data_fields+: [
    date8 {
      name: 'most_recent_duals_sep_use_date',
      title: 'Most Recent Duals SEP Use Date',
    },
  ] + std.flattenArrays([
    [
      date8 {
        name: 'cara_status_start_date_%d' % i,
        title: 'CARA Status Start Date (%d)' % i,
      },
      date8 {
        name: 'cara_status_end_date_%d' % i,
        title: 'CARA Status End Date (%d)' % i,
      },
    ]
    for i in std.range(1, 10)
  ]),
  padding_length:: 266,
}
