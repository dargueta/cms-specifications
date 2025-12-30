# SPDX-License-Identifier: BSD-3-Clause
$schema: https://datapackage.org/profiles/2.0/tableschema.json
fieldsMatch: [subset]
fields:
  - name: record_type
    title: Record Type
    type: string
    constraints:
      enum: ["DTL"]
      maxLength: 3
  - name: original_record_type
    title: Record Type
    type: string
    constraints:
      maxLength: 5
      required: true
  - name: beneficiary_id
    title: Beneficiary ID
    description: >-
      This field will contain exactly what is received in the same field of the
      beneficiary's Detail record in the related BEQ Request file.
    type: string
    constraints:
      minLength: 11
      maxLength: 12
      required: true
  - !filler 9
  - !date8
    name: beneficiary_dob
    title: Beneficiary's Date of Birth
  - !sex-code
    name: sex_code
    title: Beneficiary's Sex Code"
  - name: detail_record_sequence_number
    title: Detail Record Sequence Number
    type: integer
    constraints:
      minLength: 1
      maxLength: 7
      minimum: 0
      maximum: 9999999
      required: true
      unique: true
  - !bool-yn
    name: processed_flag
    title: Processed Flag
    constraints:
      required: true
  - !bool-yn
    name: beneficiary_matched_flag
    title: Beneficiary Matched Flag
    constraints:
      required: true
  - !date8
    name: medicare_part_a_entitlement_start_date
    title: Medicare Part A Entitlement Start Date
  - !date8
    name: medicare_part_a_entitlement_end_date
    title: Medicare Part A Entitlement End Date
  - !date8
    name: medicare_part_b_entitlement_start_date
    title: Medicare Part B Entitlement Start Date
  - !date8
    name: medicare_part_b_entitlement_end_date
    title: Medicare Part B Entitlement End Date
% for i in range(1, 11):
  - !date8
    name: part_d_enrollment_effective_date_${i}
    title: Part D Enrollment Effective Date or Employer Subsidy Start Date (Occurrence ${i})
  - !date8
    name: part_d_disenrollment_date_${i}
    title: Part D Disenrollment Date or Employer Subsidy End Date (Occurrence ${i})
% endfor
  - name: sending_entity
    title: Sending Entity
    type: string
    constraints:
      maxLength: 8
  - name: file_control_number
    title: File Control Number
    type: string
    constraints:
      maxLength: 9
      minLength: 1
      required: true
  - !date8
    name: file_creation_date
    title: File Creation Date
    constraints:
      required: true
  - !date8
    name: part_d_eligibility_start_date
    title: Part D Eligibility Start Date
    description: >-
      (Note: The 18.7 specs do not specify a format for the date field, but it's almost
      certainly YYYYMMDD as in all the other fields.)
% for i in range(1, 3):
  - !date8
    name: deemed_lis_effective_date_${i}
    title: Deemed / Low-Income Subsidy Effective Date (Occurrence ${i})
  - !date8
    name: deemed_lis_end_date_${i}
    title: Deemed / Low-Income Subsidy End Date (Occurrence ${i})
  - name: copayment_level_identifier_${i}
    title: Co-Payment Level Identifier
    type: string
    constraints:
      enum: ["1", "2", "3", "4", "5"]
      maxLength: 1
  - name: part_d_premium_subsidy_percent
    title: Part D Premium Subsidy Percent
    type: integer
    constraints:
      minimum: 25
      maximum: 100
      enum:
        - 25
        - 50
        - 75
        - 100
      maxLength: 3
    __serialization:
      justify: right
      fill: zero
% endfor
% for i in range(1, 11):
  - name: rds_part_d_indicator_${i}
    title: RDS / Part D Indicator (Occurrence ${i})
    type: string
    constraints:
      enum: ["D", "R"]
      maxLength: 1
% endfor
% for i in range(1, 21):
  - !date8
    name: start_date_${i}
    title: Start Date (Occurrence ${i})
  - name: number_of_uncovered_months_${i}
    title: Number of Uncovered Months (Occurrence ${i})
    type: integer
    constraints:
      minimum: 0
      maximum: 999
      maxLength: 3
  - name: number_of_uncovered_months_status_indicator_${i}
    title: Number of Uncovered Months Status Indicator (Occurrence ${i})
    type: string
    constraints:
      maxLength: 1
  - name: total_number_of_uncovered_months_${i}
    title: Number of Uncovered Months Status Indicator (Occurrence ${i})
    type: integer
    constraints:
      minimum: 0
      maximum: 999
      maxLength: 3
    __serialization:
      justify: right
      fill: zero
% endfor
  - !date8
    name: retrieved_date_of_birth
    title: Beneficiary's Retrieved Date of Birth
    description: As retrieved from CMS database for matching beneficiary.
  - !sex-code
    name: retrieved_sex_code
    title: "Beneficiary's Retrieved Sex Code
    description: As retrieved from CMS database for matching beneficiary.
  - name: last_name
    title: Last Name
    type: string
    constraints:
      maxLength: 40
  - name: first_name
    title: First Name
    type: string
    constraints:
      maxLength: 30
  - name: middle_initial
    title: Middle Initial
    type: string
    constraints:
      maxLength: 1
  - name: current_state_code
    title: Current State Code
    type: string
    constraints:
      maxLength: 2
  - name: current_county_code
    title: Current County Code
    type: string
    constraints:
      maxLength: 3
  - !date8
    name: date_of_death
    title: Date of Death
  - name: part_c_d_contract_number
    title: Part C/D Contract Number
    type: string
    constraints:
      maxLength: 5
  - !date8
    name: part_c_d_enrollment_start_date
    title: Part C/D Enrollment Start Date
  - !bool-yn
    name: part_d_indicator
    title: Part D Indicator
  - name: part_c_contract_number
    title: Part C Contract Number
    type: string
    constraints:
      maxLength: 5
  - !date8
    name: part_c_enrollment_start_date
    title: Part C Enrollment Start Date
  - !bool-yn
    name: part_d_indicator_2
    title: Part D Indicator
    description: >-
      This appears twice in the documentation and it's unclear what the difference is.
  - !bool-10
    name: esrd_indicator
    title: End Stage Renal Disease Indicator
  - name: part_c_pbp_number
    title: PBP Number
    description: Associated with contract number in Field 88, positions 717 - 721.
    type: string
    constraints:
      maxLength: 3
  - name: part_c_plan_type_code
    title: Plan Type Code
    description: Associated with PBP number in Field 95, positions 746 - 748
    type: string
    constraints:
      pattern: "\\d{2}"
      maxLength: 2
  - !bool-yn
    name: part_c_eghp_indicator
    title: EGHP Indicator
    description: Associated with PBP number in Field 95, positions 746 - 748
  - name: part_c_d_pbp_number
    title: PBP Number
    description: Associated with contract number in Field 91, positions 731 - 735
    type: string
    constraints:
      maxLength: 3
  - name: part_c_d_plan_type_code
    title: Plan Type Code
    description: Associated with contract number in Field 91, positions 731 - 735
    type: string
    constraints:
      pattern: "\\d{2}"
      maxLength: 2
  - !bool-yn
    name: part_c_d_eghp_indicator
    title: EGHP Indicator
    description: Associated with contract number in Field 91, positions 731 - 735
% for i in range(1, 7):
  - name: mailing_address_line_${i}
    title: Mailing Address Line ${i}
    type: string
    constraints:
      maxLength: 40
% endfor
  - name: mailing_address_city
    title: Mailing Address City
    type: string
    constraints:
      maxLength: 40
  - name: mailing_address_state
    title: Mailing Address Postal State Code
    type: string
    constraints:
      maxLength: 2
  - name: mailing_address_zip_code
    title: Mailing Address ZIP Code
    type: string
    constraints:
      maxLength: 9
  - !date8
    name: mailing_address_start_date
    title: Mailing Address Start Date
  - name: residence_address_line_1
    title: Residence Address Line 1
    type: string
    constraints:
      maxLength: 60
  - name: residence_address_city
    title: Residence Address City
    type: string
    constraints:
      maxLength: 40
  - name: residence_address_state
    title: Residence Address Postal State Code
    type: string
    constraints:
      maxLength: 2
  - name: residence_address_zip_code
    title: Residence Address ZIP Code
    type: string
    constraints:
      maxLength: 9
  - !date8
    name: residence_address_start_date
    title: Residence Address Start Date
% for i in range(1, 11):
  - !date8
    name: medicare_plan_ineligibility_due_to_incarceration_start_date_${i}
    title: Medicare Plan Ineligibility Due to Incarceration Start Date (${i})
  - !date8
    name: medicare_plan_ineligibility_due_to_incarceration_end_date_${i}
    title: Medicare Plan Ineligibility Due to Incarceration End Date (${i})
% endfor
% for i in range(1, 11):
  - !date8
    name: medicare_plan_ineligibility_due_to_not_lawful_presence_start_date_${i}
    title: Medicare Plan Ineligibility Due to Not Lawful Presence Start Date (${i})
  - !date8
    name: medicare_plan_ineligibility_due_to_not_lawful_presence_end_date_${i}
    title: Medicare Plan Ineligibility Due to Not Lawful Presence End Date (${i})
% endfor
