// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/9.2/records/detail.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: std.flattenArrays([
    [
      pcug.date8 {
        name: 'medicare_plan_ineligibility_due_to_incarceration_start_date_%d' % i,
        title: 'Medicare Plan Ineligibility Due to Incarceration Start Date (%d)' % i,
      },
      pcug.date8 {
        name: 'medicare_plan_ineligibility_due_to_incarceration_end_date_%d' % i,
        title: 'Medicare Plan Ineligibility Due to Incarceration End Date (%d)' % i,
      },
    ]
    for i in std.range(1, 10)
  ]) + std.flattenArrays([
    [
      pcug.date8 {
        name: 'medicare_plan_ineligibility_due_to_not_lawful_presence_start_date_%d' % i,
        title: 'Medicare Plan Ineligibility Due to Not Lawful Presence Start Date (%d)' % i,
      },
      pcug.date8 {
        name: 'medicare_plan_ineligibility_due_to_not_lawful_presence_end_date_%d' % i,
        title: 'Medicare Plan Ineligibility Due to Not Lawful Presence End Date (%d)' % i,
      },
    ]
    for i in std.range(1, 10)
  ]),
  padding_length:: 5,
}
