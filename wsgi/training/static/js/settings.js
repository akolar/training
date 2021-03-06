// Generated by CoffeeScript 1.9.1
$(function() {
  var check_pass;
  $('.settings form').submit(false);
  $('[data-action="default"]').change(function() {
    var field;
    field = $(this);
    return $.ajax({
      url: '/settings/save/' + this.id,
      method: 'PUT',
      data: {
        value: field.val()
      },
      success: function(data, textStatus, jqXHR) {
        var marker;
        if (data.success) {
          marker = field.closest('.row').find('.saved');
          marker.addClass('active');
          return setTimeout((function() {
            return marker.removeClass('active');
          }), 2000);
        }
      }
    });
  });
  check_pass = function() {
    var cpass, pass1, pass2;
    cpass = $('#cpasswd').val();
    pass1 = $('#npasswd1').val();
    pass2 = $('#npasswd2').val();
    return (cpass !== '') && (pass1 !== '') && (pass1 === pass2);
  };
  $('input[type="password"]').change(function() {
    if (check_pass()) {
      return $('button[data-action="set-passwd"]').removeAttr('disabled');
    } else {
      return $('button[data-action="set-passwd"]').attr('disabled', '');
    }
  });
  $('button[data-action="set-passwd"]').click(function() {
    var cpass, pass1, pass2;
    cpass = $('#cpasswd').val();
    pass1 = $('#npasswd1').val();
    pass2 = $('#npasswd2').val();
    return $.ajax({
      url: '/settings/save/password',
      method: 'PUT',
      data: {
        current: cpass,
        "new": pass1
      },
      success: function(data, textStatus, jqXHR) {
        var marker;
        $('.text-danger').addClass('hidden');
        if (data.success) {
          marker = field.closest('.row').find('.saved');
          marker.addClass('active');
          return setTimeout((function() {
            return marker.removeClass('active');
          }), 2000);
        } else {
          return $('.' + data.reason).removeClass('hidden');
        }
      }
    });
  });
  $('[data-action="avatar"]').click(function() {
    var data;
    data = new FormData();
    data.append('avatar', $('[name="avatar"]')[0].files[0]);
    $.ajax({
      url: '/settings/save/avatar',
      method: 'POST',
      data: data,
      cache: false,
      processData: false,
      contentType: false,
      success: function(data, textStatus, jqXHR) {
        return location.reload();
      }
    });
    return false;
  });
  return $('[data-action="goals"]').change(function() {
    var field, params;
    field = $(this);
    params = this.name.split('_');
    return $.ajax({
      url: '/goals/set/' + params[0],
      data: {
        objective: params[1],
        value: field.val()
      },
      method: 'PUT',
      success: function(data, textStatus, jqXHR) {
        return console.log(data);
      }
    });
  });
});
