// SPDX-License-Identifier: BSD-3-Clause
local detail = import 'bqn4/common/records/detail/9.2.jsonnet';
local header = import 'bqn4/common/records/header/9.2.jsonnet';
local trailer = import 'bqn4/common/records/trailer/9.2.jsonnet';
local file = import 'bqn4/common/whole_file.jsonnet';

file('9.2', header, detail, trailer)
