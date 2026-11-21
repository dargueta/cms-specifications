// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/records/detail/10.3.jsonnet';


base {
  data_fields+: [
    {
      name: 'Active MBI',
      description: "The MBI from the beneficiary's active Beneficiary MBI period. The value is "
                   + 'a system-generated identifier used internally and externally to uniquely '
                   + 'identify the beneficiary in the Medicare database.',
      logicalType: 'string',
      logicalTypeOptions: {
        minLength: 11,
        maxLength: 11,
      },
      required: true,
      physicalName: 'active_mbi',
    },
  ],
  padding_length:: 434,
}
