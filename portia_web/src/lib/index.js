const format_obj = new Intl.NumberFormat()

function number_format(value) {
  return format_obj.format(value)
}

export { number_format }