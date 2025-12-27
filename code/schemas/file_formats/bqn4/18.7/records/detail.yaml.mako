# SPDX-License-Identifier: BSD-3-Clause
<%def name="render_sex_code(field_name, title='Sex Code', description='')">\
{
    "name": "${field_name}",
    "title": "${title}",
% if description:
    "description": "${description}",
% endif
    "type": "string",
    "rdfType": "https://schema.org/GenderType",
    "categories": [
        {"value": "0", "label": "Unknown"},
        {"value": "1", "label": "Male"},
        {"value": "2", "label": "Female"}
    ]
}
</%def>
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
  - name: _filler
    type: string
    constraints:
      enum: [""]
      maxLength: 9
  - name: beneficiary_dob
    title: Beneficiary's Date of Birth
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
  - ${render_sex_code("sex_code", "Beneficiary's Sex Code")}
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
  - name: processed_flag
    title: Processed Flag
    type: boolean
    trueValues: ["Y"]
    falseValues: ["N"]
    constraints:
      required: true
  - name: beneficiary_matched_flag
    title: Beneficiary Matched Flag
    type: boolean
    trueValues: ["Y"]
    falseValues: ["N"]
    constraints:
      required: true
  - name: medicare_part_a_entitlement_start_date
    title: Medicare Part A Entitlement Start Date
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
  - name: medicare_part_a_entitlement_end_date
    title: Medicare Part A Entitlement End Date
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
  - name: medicare_part_b_entitlement_start_date
    title: Medicare Part B Entitlement Start Date
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
  - name: medicare_part_b_entitlement_end_date
    title: Medicare Part B Entitlement End Date
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
% for i in range(1, 11):
  - name: part_d_enrollment_effective_date_${i}
    title: Part D Enrollment Effective Date or Employer Subsidy Start Date (Occurrence ${i})
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
  - name: part_d_disenrollment_date_${i}
    title: Part D Disenrollment Date or Employer Subsidy End Date (Occurrence ${i})
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
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
  - name: file_creation_date
    title: File Creation Date
    type: date
    format: "%Y%m%d"
    constraints:
      maxLength: 8
      required: true
  - name: part_d_eligibility_start_date
    title: Part D Eligibility Start Date
    description: >-
      (Note: The 18.7 specs do not specify a format for the date field, but it's almost
      certainly YYYYMMDD as in all the other fields.)
    type: date
    format: "%Y%m%d"
% for i in range(1, 3):
  - name: deemed_lis_effective_date_${i}
    title: Deemed / Low-Income Subsidy Effective Date (Occurrence ${i})
    type: date
    format: "%Y%m%d"
  - name: deemed_lis_end_date_${i}
    title: Deemed / Low-Income Subsidy End Date (Occurrence ${i})
    type: date
    format: "%Y%m%d"
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
  - name: start_date_${i}
    title: Start Date (Occurrence ${i})
    type: date
    format: "%Y%m%d"
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
  - name: retrieved_date_of_birth
    title: Beneficiary's Retrieved Date of Birth
    description: As retrieved from CMS database for matching beneficiary.
    type: date
    format: "%Y%m%d"
  - ${render_sex_code("retrieved_sex_code", "Beneficiary's Retrieved Sex Code", "As retrieved from CMS database for matching beneficiary.")}
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
  - name: date_of_death
    title: Date of Death
    type: date
    format: "%Y%m%d"
  - name: part_c_d_contract_number
    title: Part C/D Contract Number
    type: string
    constraints:
      maxLength: 5
  - name: part_c_d_enrollment_start_date
    title: Part C/D Enrollment Start Date
    type: date
    format: "%Y%m%d"
  - name: part_d_indicator
    title: Part D Indicator
    type: boolean
    trueValues: ["Y"]
    falseValues: ["N"]
