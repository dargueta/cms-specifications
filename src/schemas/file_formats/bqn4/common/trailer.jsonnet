// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

function(filler_size) {
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    pcug.const('record_type', 'CMSBEQRT'),
    pcug.const('sending_entity', 'MBD     ') {
      title: 'Sending Entity',
      rdfType: 'https://schema.org/Organization',
    },
    pcug.date8 {
      name: 'file_creation_date',
      title: 'File Creation Date',
      constraints: {
        required: true,
      },
    },
    {
      name: 'file_control_number',
      title: 'File Control Number',
      type: 'string',
      constraints: {
        maxLength: 9,
        minLength: 1,
        required: true,
      },
    },
    {
      name: 'record_count',
      title: 'Record Count',
      type: 'integer',
      constraints: {
        minimum: 1,
        maximum: 9999999,
        minLength: 7,
        maxLength: 7,
        required: true,
      },
      __metadata__: {
        serialization: {
          align: 'right',
          padding_character: '0',
        },
      },
    },
    pcug.filler('record_padding', filler_size),
  ],
}
