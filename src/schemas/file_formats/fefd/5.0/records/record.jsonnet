// SPDX-License-Identifier: BSD-3-Clause
local beneficiary_identifier = import 'beneficiary_identifier.jsonnet';
local const = import 'const.jsonnet';
local date8 = import 'date8.jsonnet';
local enrollment_source_type_code = import 'enrollment_source_type_code.jsonnet';
local filler = import 'filler.jsonnet';
local sex_code = import 'sex_code.jsonnet';

{
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    beneficiary_identifier,
    {
      name: 'surname',
      title: 'Surname',
      type: 'string',
      constraints: {
        maxLength: 12,
        required: true,
      },
    },
    {
      name: 'first_name',
      title: 'First Name',
      type: 'string',
      constraints: {
        maxLength: 7,
        required: true,
      },
    },
    {
      name: 'middle_initial',
      title: 'Middle Initial',
      type: 'string',
      constraints: {
        maxLength: 1,
      },
    },
    sex_code,
    date8 {
      name: 'date_of_birth',
    },
    filler('medicaid_indicator', 1),  // Medicaid indicator
    {
      name: 'plan_contract_number',
      title: 'Plan Contract Number',
      type: 'string',
      constraints: {
        maxLength: 5,
      },
    },
    {
      name: 'state_code',
      title: 'Beneficiary State Code',
      type: 'string',
      constraints: {
        minLength: 2,
        maxLength: 2,
      },
    },
    {
      name: 'county_code',
      title: 'Beneficiary County Code',
      type: 'string',
      constraints: {
        minLength: 3,
        maxLength: 3,
      },
    },
    filler('disability_indicator', 1),  // Disability indicator
    filler('hospice_indicator', 1),  // Hospice indicator
    filler('institutional_nhc_hcbs_indicator', 1),  // Institutional/NHC/HCBS Indicator
    filler('esrd_indicator', 1),  // ESRD Indicator
    const('transaction_reply_code', '999'),  // Transaction Reply Code
    {
      name: 'transaction_code',
      type: 'string',
      constraints: {
        maxLength: 2,
        missingValues: ['01'],
      },
    },
    filler('entitlement_type_code', 1),  // Entitlement type code
    date8 {
      name: 'effective_date',
      title: 'Effective Date',
    },
    filler('wa_indicator', 1),  // WA Indicator
    {
      name: 'pbp_id',
      title: 'Plan Benefit Package (PBP) ID',
      type: 'string',
      constraints: {
        maxLength: 3,
      },
    },
    filler('race_code', 1),  // "Race code" in later file versions
    date8 {
      name: 'transaction_date',
      title: 'Transaction Date',
      constraints: {
        required: true,
      },
    },
    filler('_filler_1', 1),
    date8 {
      name: 'subsidy_end_date',
      title: 'Subsidy End Date',
      description: 'End date of LIS Period (Present if Beneficiary is deemed for the full year, or if the Beneficiary is losing Low Income status before the end of the current year.)',
    },
    filler('subsidy_end_date_padding', 4),  // `subsidy_end_date` is listed as 12 spaces, but has an 8-digit year.
    filler('district_office_code', 3),  // District office code
    filler('_filler_2', 8),  // (No description)
    filler('_filler_3', 8),  // (No description)
    filler('source_id', 5),  // Source ID
    filler('prior_plan_benefit_package_id', 3),  // Prior plan benefit package ID
    filler('application_date', 8),  // Application date
    filler('_filler_4', 2),
    filler('out_of_area_flag', 1),  // Out of area flag
    {
      name: 'segment_number',
      title: 'Segment Number',
      type: 'string',
      constraints: {
        maxLength: 3,
        missingValues: ['000', ''],
      },
      __metadata__: {
        serialization: {
          align: 'right',
          padding_character: '0',
        },
      },
    },
    // TODO (dargueta): Determine if the decimal is present or implicit.
    {
      name: 'part_c_beneficiary_premium',
      title: 'Part C Beneficiary Premium',
      description: 'Part C Premium Amount; the amount submitted on the enrollment record for Part C premium.',
      type: 'number',
      constraints: {
        minimum: 0,
        maximum: 99999999,
        decimalChar: '',
      },
    },
    // TODO (dargueta): Determine if the decimal is present or implicit.
    {
      name: 'part_d_beneficiary_premium',
      title: 'Part D Beneficiary Premium',
      description: 'Part D Premium Amount; the Part D Total Premium Net of Rebate from the HPMS file.',
      type: 'number',
      constraints: {
        minimum: 0,
        maximum: 99999999,
        decimalChar: '',
      },
    },
    filler('election_type', 1),  // Election type
    enrollment_source_type_code {
      name: 'enrollment_source_code',
    },
    filler('part_d_opt_out_flag', 1),  // Part D opt-out flag
    {
      name: 'premium_withhold_option_parts_c_d',
      title: 'Premium Withhold Option -- Parts C/D',
      type: 'string',
      categories: [
        { value: 'D', label: 'Direct bill' },
        { value: 'S', label: 'SSA withhold' },
        { value: 'N', label: 'No premium' },
      ],
    },
    filler('number_of_uncovered_months', 3),  // Number of uncovered months
    filler('creditable_coverage_flag', 1),  // Creditable coverage flag
    filler('employer_subsidy_override_flag', 1),  // Employer subsidy override flag
    filler('rx_id', 20),  // Rx ID
    filler('rx_group', 15),  // Rx Group
    filler('secondary_drug_insurance_flag', 1),  // Secondary drug insurance flag
    filler('secondary_rx_id', 20),  // Secondary Rx ID
    filler('secondary_rx_group', 15),  // Secondary Rx Group
    filler('eghp', 1),  // EGHP
    {
      name: 'part_d_lips_level',
      title: 'Part D LIPS Level',
      type: 'integer',
      constraints: {
        minimum: 0,
        maximum: 100,
      },
      __metadata__: {
        serialization: {
          align: 'right',
          padding_character: '0',
        },
      },
    },
    {
      name: 'low_income_copay_category',
      title: 'Low-Income Co-Pay Category',
      type: 'string',
      categories: [
        { value: '0', label: 'None, not low-income' },
        { value: '1', label: 'High' },
        { value: '2', label: 'Low' },
        { value: '3', label: '$0' },
        { value: '4', label: '15%' },
        { value: '5', label: 'Unknown' },
      ],
    },
    date8 {
      name: 'low_income_copay_effective_date',
      title: 'Low-Income Co-Pay Effective Date',
    },
    filler('part_d_lep_amount', 8),  // Part D LEP amount
    filler('part_d_lep_waived_amount', 8),  // Part D LEP waived amount
    filler('part_d_lep_subsidy_amount', 8),  // Part D LEP subsidy amount
    // TODO (dargueta): Determine if the decimal is present or implicit.
    {
      name: 'low_income_part_d_premium_subsidy_amount',
      title: 'Low-Income Part D Premium Subsidy Amount',
      type: 'number',
      constraints: {
        minimum: 0,
        maximum: 99999999,
        decimalChar: '',
      },
    },
  ],
}
