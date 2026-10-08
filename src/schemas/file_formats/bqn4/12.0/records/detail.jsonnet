// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/10.3/records/detail.jsonnet';


base {
  data_fields+: [
    {
      name: 'active_mbi',
      title: 'Active MBI',
      description: "The MBI from the beneficiary's active Beneficiary MBI period. The value is "
                   + 'a system-generated identifier used internally and externally to uniquely '
                   + 'identify the beneficiary in the Medicare database.',
      type: 'string',
      constraints: {
        minLength: 11,
        maxLength: 11,
        required: true,
      },
    },
  ],
  padding_length:: 434,
}
