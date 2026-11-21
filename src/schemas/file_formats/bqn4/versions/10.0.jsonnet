// SPDX-License-Identifier: BSD-3-Clause
local detail = import 'bqn4/common/records/detail/10.0.jsonnet';
local header = import 'bqn4/common/records/header/9.2.jsonnet';  // Unchanged
local trailer = import 'bqn4/common/records/trailer/9.2.jsonnet';  // Unchanged
local file = import 'bqn4/common/whole_file.jsonnet';

file('10.0', header, detail, trailer)
