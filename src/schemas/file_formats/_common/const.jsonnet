function(name, string_value) {
  name: name,
  type: 'string',
  constraints: {
    enum: [string_value],
    minLength: std.length(string_value),
    maxLength: std.length(string_value),
    required: true,
  },
}
