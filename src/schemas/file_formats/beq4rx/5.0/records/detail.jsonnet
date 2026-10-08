// SPDX-License-Identifier: BSD-3-Clause
local beneficiary_identifier = import 'beneficiary_identifier.jsonnet';
local const = import 'const.jsonnet';
local date8 = import 'date8.jsonnet';
local filler = import 'filler.jsonnet';
local sex_code = import 'sex_code.jsonnet';

{
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    const('record_type', 'DTL01'),
    beneficiary_identifier,
    filler('_filler_1', 9),
    date8 {
      name: 'dob',
      title: 'DOB',
      description: "The date of the beneficiary's birth.",
      constraints: {
        required: true,
      },
    },
    sex_code,
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
    filler('trailer', 708),
  ],
}
