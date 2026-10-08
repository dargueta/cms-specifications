// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/5.1/records/detail.jsonnet';
local bool_10 = import 'bool_10.jsonnet';
local bool_yn = import 'bool_yn.jsonnet';
local plan_type_code = import 'plan_type_code.jsonnet';


base {
  data_fields+: [
    bool_10 {
      name: 'esrd_indicator',
      title: 'End Stage Renal Disease Indicator',
    },
    {
      name: 'part_c_pbp_number',
      title: 'PBP Number',
      description: 'Associated with contract number in Field 88, positions 717 - 721.',
      type: 'string',
      constraints: {
        maxLength: 3,
      },
    },
    plan_type_code {
      name: 'part_c_plan_type_code',
      title: 'Plan Type Code',
      description: 'Associated with PBP number in Field 95, positions 746 - 748',
    },
    bool_yn {
      name: 'part_c_eghp_indicator',
      title: 'EGHP Indicator',
      description: 'Associated with PBP number in Field 95, positions 746 - 748',
    },
    {
      name: 'part_c_d_pbp_number',
      title: 'PBP Number',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
      type: 'string',
      constraints: {
        maxLength: 3,
      },
    },
    plan_type_code {
      name: 'part_c_d_plan_type_code',
      title: 'Plan Type Code',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
    },
    bool_yn {
      name: 'part_c_d_eghp_indicator',
      title: 'EGHP Indicator',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
    },
  ],
  padding_length:: 743,
}
