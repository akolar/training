$ ->
    $('[data-tc]').change ->
        multies = [3600, 60, 1]
        vals = [do $('#id_time_hrs').val, do $('#id_time_min').val, do $('#id_time_sec').val]

        total = 0
        for val, i in vals
            v = if val then parseInt val else 0
            total += v * multies[i]

        $('#id_elapsed').val total
