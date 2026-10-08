function(name, width) {
  name: name,
  title: 'Filler',
  type: 'string',
  constraints: {
    enum: [''],
    maxLength: width,
  },
}
