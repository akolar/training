$ ->
    $('.settings form').submit false
    $('[data-action="default"]').change ->
        field = $(this)

        $.ajax
            url: '/settings/save/' + this.id
            method: 'PUT'
            data: { value: do field.val }
            success: (data, textStatus, jqXHR) ->
                if data.success
                    marker = field.closest('.row').find '.saved'
                    marker.addClass 'active'
                    setTimeout ( ->
                        marker.removeClass 'active'
                    ), 2000

    check_pass = ->
        cpass = do $('#cpasswd').val
        pass1 = do $('#npasswd1').val
        pass2 = do $('#npasswd2').val

        return (cpass != '') and (pass1 != '') and (pass1 == pass2)

    $('input[type="password"]').change ->
        if do check_pass
            $('button[data-action="set-passwd"]').removeAttr 'disabled'
        else
            $('button[data-action="set-passwd"]').attr 'disabled', ''

    $('button[data-action="set-passwd"]').click ->
        cpass = do $('#cpasswd').val
        pass1 = do $('#npasswd1').val
        pass2 = do $('#npasswd2').val

        $.ajax
            url: '/settings/save/password'
            method: 'PUT'
            data: {current: cpass, new: pass1}
            success: (data, textStatus, jqXHR) ->
                $('.text-danger').addClass 'hidden'

                if data.success
                    marker = field.closest('.row').find '.saved'
                    marker.addClass 'active'
                    setTimeout ( ->
                        marker.removeClass 'active'
                    ), 2000
                else
                    $('.' + data.reason).removeClass 'hidden'

    $('[data-action="avatar"]').click ->
        data = new FormData()
        data.append 'avatar', $('[name="avatar"]')[0].files[0]

        $.ajax
            url: '/settings/save/avatar'
            method: 'POST'
            data: data
            cache: false
            processData: false
            contentType: false
            success: (data, textStatus, jqXHR) ->
                do location.reload

        return false

    $('[data-action="goals"]').change ->
        field = $(this)
        params = this.name.split('_')

        $.ajax
            url: '/goals/set/' + params[0]
            data:
                objective: params[1]
                value: do field.val
            method: 'PUT'
            success: (data, textStatus, jqXHR) ->
                console.log data
