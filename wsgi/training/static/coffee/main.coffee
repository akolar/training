getCookie = (name) ->
    cookieValue = null

    if document.cookie and (document.cookie != '')
        cookies = document.cookie.split ';'
        for cookie in cookies
            c = $.trim cookie

            if (c.substring 0, (name.length + 1)) == (name + '=')
                cookieValue = decodeURIComponent cookie.substring(name.length + 2)
                break

    return cookieValue


csrftoken = getCookie('csrftoken')


csrfSafeMethod = (method) ->
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test method;


$.ajaxSetup
    beforeSend: (xhr, settings) ->
        if !csrfSafeMethod settings.type and not this.crossDomain
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
