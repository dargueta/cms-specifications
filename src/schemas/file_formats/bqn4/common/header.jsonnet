// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

function(filler_size) {
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    pcug.const('record_type', 'CMSBEQRH'),
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
    pcug.filler('record_padding', filler_size),
  ],
}
