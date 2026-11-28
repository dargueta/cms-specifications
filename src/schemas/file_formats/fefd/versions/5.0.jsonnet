// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  apiVersion: '3.2.0',
  kind: 'DataContract',

  name: 'Full Enrollment Data File',
  id: '190a50bd-102f-4201-9272-987604d3ac05',
  version: '5.0',
  schema: [
    {
      id: 'data',
      physicalName: 'data',
      properties: [
        pcug.beneficiary_identifier,
        {
          name: 'Surname',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 12,
          },
          required: true,
          physicalName: 'surname',
        },
        {
          name: 'First Name',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 7,
          },
          required: true,
          physicalName: 'first_name',
        },
        {
          name: 'Middle Initial',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 1,
          },
          physicalName: 'middle_initial',
        },
        pcug.sex_code,
        pcug.date8 {
          physicalName: 'date_of_birth',
        },
        pcug.filler('medicaid_indicator', 1),  // Medicaid indicator
        {
          name: 'Plan Contract Number',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 5,
          },
          physicalName: 'plan_contract_number',
        },
        {
          name: 'Beneficiary State Code',
          logicalType: 'string',
          logicalTypeOptions: {
            minLength: 2,
            maxLength: 2,
          },
          physicalName: 'state_code',
        },
        {
          name: 'Beneficiary County Code',
          logicalType: 'string',
          logicalTypeOptions: {
            minLength: 3,
            maxLength: 3,
          },
          physicalName: 'county_code',
        },
        pcug.filler('disability_indicator', 1),  // Disability indicator
        pcug.filler('hospice_indicator', 1),  // Hospice indicator
        pcug.filler('institutional_nhc_hcbs_indicator', 1),  // Institutional/NHC/HCBS Indicator
        pcug.filler('esrd_indicator', 1),  // ESRD Indicator
        pcug.const('transaction_reply_code', '999'),  // Transaction Reply Code
        {
          physicalName: 'transaction_code',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 2,
          },
          customProperties: {
            serialization: {
              nullSentinels: ['01'],
            },
          },
        },
        pcug.filler('entitlement_type_code', 1),  // Entitlement type code
        pcug.date8 {
          physicalName: 'effective_date',
          name: 'Effective Date',
        },
        pcug.filler('wa_indicator', 1),  // WA Indicator
        {
          name: 'Plan Benefit Package (PBP) ID',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 3,
          },
          physicalName: 'pbp_id',
        },
        pcug.filler('race_code', 1),  // "Race code" in later file versions
        pcug.date8 {
          name: 'Transaction Date',
          physicalName: 'transaction_date',
          required: true,
        },
        pcug.filler('_filler_1', 1),
        pcug.date8 {
          name: 'Subsidy End Date',
          description: 'End date of LIS Period (Present if Beneficiary is deemed for the full year, or if the Beneficiary is losing Low Income status before the end of the current year.)',
          physicalName: 'subsidy_end_date',
        },
        pcug.filler('subsidy_end_date_padding', 4),  // `subsidy_end_date` is listed as 12 spaces, but has an 8-digit year.
        pcug.filler('district_office_code', 3),  // District office code
        pcug.filler('_filler_2', 8),  // (No description)
        pcug.filler('_filler_3', 8),  // (No description)
        pcug.filler('source_id', 5),  // Source ID
        pcug.filler('prior_plan_benefit_package_id', 3),  // Prior plan benefit package ID
        pcug.filler('application_date', 8),  // Application date
        pcug.filler('_filler_4', 2),
        pcug.filler('out_of_area_flag', 1),  // Out of area flag
        {
          name: 'Segment Number',
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 3,
          },
          physicalName: 'segment_number',
          customProperties: {
            serialization: {
              nullSentinels: ['000', ''],
              align: 'right',
              padding_character: '0',
            },
          },
        },
        // TODO (dargueta): Determine if the decimal is present or implicit.
        {
          name: 'Part C Beneficiary Premium',
          description: 'Part C Premium Amount; the amount submitted on the enrollment record for Part C premium.',
          logicalType: 'number',
          logicalTypeOptions: {
            minimum: 0,
            maximum: 99999999,
          },
          physicalName: 'part_c_beneficiary_premium',
          customProperties: {
            serialization: {
              length: 8,
              decimalChar: '',
            },
          },
        },
        // TODO (dargueta): Determine if the decimal is present or implicit.
        {
          name: 'Part D Beneficiary Premium',
          description: 'Part D Premium Amount; the Part D Total Premium Net of Rebate from the HPMS file.',
          logicalType: 'number',
          logicalTypeOptions: {
            minimum: 0,
            maximum: 99999999,
          },
          physicalName: 'part_d_beneficiary_premium',
          customProperties: {
            serialization: {
              length: 8,
              decimalChar: '',
            },
          },
        },
        pcug.filler('election_type', 1),  // Election type
        pcug.enrollment_source_type_code {
          physicalName: 'enrollment_source_code',
        },
        pcug.filler('part_d_opt_out_flag', 1),  // Part D opt-out flag
        {
          name: 'Premium Withhold Option -- Parts C/D',
          logicalType: 'string',
          enum: [
            { value: 'D', label: 'Direct bill' },
            { value: 'S', label: 'SSA withhold' },
            { value: 'N', label: 'No premium' },
          ],
          physicalName: 'premium_withhold_option_parts_c_d',
          customProperties: {
            serialization: {
              length: 1,
            },
          },
        },
        pcug.filler('number_of_uncovered_months', 3),  // Number of uncovered months
        pcug.filler('creditable_coverage_flag', 1),  // Creditable coverage flag
        pcug.filler('employer_subsidy_override_flag', 1),  // Employer subsidy override flag
        pcug.filler('rx_id', 20),  // Rx ID
        pcug.filler('rx_group', 15),  // Rx Group
        pcug.filler('secondary_drug_insurance_flag', 1),  // Secondary drug insurance flag
        pcug.filler('secondary_rx_id', 20),  // Secondary Rx ID
        pcug.filler('secondary_rx_group', 15),  // Secondary Rx Group
        pcug.filler('eghp', 1),  // EGHP
        {
          name: 'Part D LIPS Level',
          physicalName: 'part_d_lips_level',
          logicalType: 'integer',
          logicalTypeOptions: {
            minimum: 0,
            maximum: 100,
          },
          customProperties: {
            serialization: {
              length: 3,
              align: 'right',
              padding_character: '0',
            },
          },
        },
        {
          name: 'Low-Income Co-Pay Category',
          logicalType: 'string',
          enum: [
            { value: '0', label: 'None, not low-income' },
            { value: '1', label: 'High' },
            { value: '2', label: 'Low' },
            { value: '3', label: '$0' },
            { value: '4', label: '15%' },
            { value: '5', label: 'Unknown' },
          ],
          physicalName: 'low_income_copay_category',
          customProperties: {
            serialization: {
              length: 1,
            },
          },
        },
        pcug.date8 {
          name: 'Low-Income Co-Pay Effective Date',
          physicalName: 'low_income_copay_effective_date',
        },
        pcug.filler('part_d_lep_amount', 8),  // Part D LEP amount
        pcug.filler('part_d_lep_waived_amount', 8),  // Part D LEP waived amount
        pcug.filler('part_d_lep_subsidy_amount', 8),  // Part D LEP subsidy amount
        // TODO (dargueta): Determine if the decimal is present or implicit.
        {
          name: 'Low-Income Part D Premium Subsidy Amount',
          logicalType: 'number',
          logicalTypeOptions: {
            minimum: 0,
            maximum: 99999999,
          },
          physicalName: 'low_income_part_d_premium_subsidy_amount',
          customProperties: {
            serialization: {
              length: 8,
              decimalChar: '',
            },
          },
        },
      ],
    },
  ],
}
