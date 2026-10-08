// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/10.0/records/detail.jsonnet';
local bool_yn = import 'bool_yn.jsonnet';
local date8 = import 'date8.jsonnet';
local enrollment_source_type_code = import 'enrollment_source_type_code.jsonnet';
local plan_type_code = import 'plan_type_code.jsonnet';


base {
  data_fields+: [
    enrollment_source_type_code {
      name: 'current_enrollment_source_type_code_95',
      title: 'Current Enrollment Source Type Code',
      description: 'Associated with PBP number in Field 95, positions 746 - 748.',
    },
    enrollment_source_type_code {
      name: 'current_enrollment_source_type_code_98',
      title: 'Current Enrollment Source Type Code',
      description: 'Associated with PBP number in Field 98, positions 752 - 754.',
    },
    {
      name: 'prior_part_c_d_contract_number',
      title: 'Prior Part C/D Contract Number',
      type: 'string',
      constraints: {
        maxLength: 5,
      },
    },
    date8 {
      name: 'prior_part_c_d_enrollment_start_date',
      title: 'Prior Part C/D Enrollment Start Date',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
    },
    date8 {
      name: 'prior_part_c_d_enrollment_disenrollment_date',
      title: 'Prior Part C/D Disenrollment Date',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
    },
    bool_yn {
      name: 'prior_part_d_indicator',
      title: 'Prior Part D Indicator',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
    },
    {
      name: 'prior_pbp_number',
      title: 'Prior PBP Number',
      description: 'Associated with Contract Number in Field 158, positions 1498-1502.',
      type: 'string',
      constraints: {
        maxLength: 3,
      },
    },
    plan_type_code {
      name: 'prior_plan_type_code',
      title: 'Prior Plan Type Code',
    },
    bool_yn {
      name: 'prior_eghp_indicator',
      title: 'Prior EGHP Indicator',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
    },
    enrollment_source_type_code {
      name: 'prior_enrollment_source_type_code',
      title: 'Prior Enrollment Source Type Code',
      description: 'Associated with PBP Number in positions 1520-1522.',
    },
    {
      name: 'prior_part_c_contract_number',
      title: 'Prior Part C Contract Number',
      type: 'string',
      constraints: {
        maxLength: 5,
      },
    },
    date8 {
      name: 'prior_part_c_enrollment_start_date',
      title: 'Prior Part C Enrollment Start Date',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
    date8 {
      name: 'prior_part_c_enrollment_disenrollment_date',
      title: 'Prior Part C Disenrollment Date',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
    bool_yn {
      name: 'prior_part_d_indicator',
      title: 'Prior Part D Indicator',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
    {
      name: 'prior_pbp_number',
      title: 'Prior PBP Number',
      description: 'Associated with Contract Number in Field 166, positions 1527-1531.',
      type: 'string',
      constraints: {
        maxLength: 3,
      },
    },
    plan_type_code {
      name: 'prior_plan_type_code',
      title: 'Prior Plan Type Code',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
    bool_yn {
      name: 'prior_eghp_indicator',
      title: 'Prior EGHP Indicator',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
    enrollment_source_type_code {
      name: 'prior_enrollment_source_type_code',
      title: 'Prior Enrollment Source Type Code',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
    },
  ],
  padding_length:: 455,
}
