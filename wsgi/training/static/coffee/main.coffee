getCookie = (name) ->
    cookieValue = null

    if document.cookie and (document.cookie != '')
        cookies = document.cookie.split ';'
        for cookie in cookies
            c = $.trim cookie

            if (c.substring 0, (name.length + 1)) == (name + '=')
                cookieValue = decodeURIComponent cookie.substring(name.length + 1)
                break

    return cookieValue


csrftoken = getCookie('csrftoken')

csrfSafeMethod = (method) ->
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test method;


$.ajaxSetup
    beforeSend: (xhr, settings) ->
        if !csrfSafeMethod settings.type and not this.crossDomain
            xhr.setRequestHeader("X-CSRFToken", csrftoken)


if SI_UNITS?
    UNITS =
        speed: if SI_UNITS then 'km/h' else 'mi/h'
        height: if SI_UNITS then 'm' else 'ft'
        distance: if SI_UNITS then 'km' else 'mi'
        temperature: if SI_UNITS then 'C' else 'F'
        per_min: '/ min'
        percent: '%'
