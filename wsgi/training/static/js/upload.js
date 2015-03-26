// Generated by CoffeeScript 1.9.1
$(function() {
  return $('[data-tc]').change(function() {
    var i, j, len, multies, total, v, val, vals;
    multies = [3600, 60, 1];
    vals = [$('#id_time_hrs').val(), $('#id_time_min').val(), $('#id_time_sec').val()];
    total = 0;
    for (i = j = 0, len = vals.length; j < len; i = ++j) {
      val = vals[i];
      v = val ? parseInt(val) : 0;
      total += v * multies[i];
    }
    return $('#id_elapsed').val(total);
  });
});