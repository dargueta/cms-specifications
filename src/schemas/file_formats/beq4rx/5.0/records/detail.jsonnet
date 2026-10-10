// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    pcug.const('record_type', 'DTL01'),
    pcug.beneficiary_identifier,
    pcug.filler('_filler_1', 9),
    pcug.date8 {
      name: 'dob',
      title: 'DOB',
      description: "The date of the beneficiary's birth.",
      constraints: {
        required: true,
      },
    },
    pcug.sex_code,
    {
      name: 'detail_record_sequence_number',
      title: 'Detail Record Sequence Number',
      description: 'A unique number assigned by the Sending Entity to the Detail Record.',
      type: 'integer',
      constraints: {
        minLength: 1,
        maxLength: 7,
        minimum: 0,
        maximum: 9999999,
        required: true,
        unique: true,
      },
    },
    pcug.filler('trailer', 708),
  ],
}
