// Generated by CoffeeScript 1.9.1
var UNITS, csrfSafeMethod, csrftoken, getCookie;

getCookie = function(name) {
  var c, cookie, cookieValue, cookies, i, len;
  cookieValue = null;
  if (document.cookie && (document.cookie !== '')) {
    cookies = document.cookie.split(';');
    for (i = 0, len = cookies.length; i < len; i++) {
      cookie = cookies[i];
      c = $.trim(cookie);
      if ((c.substring(0, name.length + 1)) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 2));
        break;
      }
    }
  }
  return cookieValue;
};

csrftoken = getCookie('csrftoken');

csrfSafeMethod = function(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
};

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type && !this.crossDomain)) {
      return xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

if (typeof SI_UNITS !== "undefined" && SI_UNITS !== null) {
  UNITS = {
    speed: SI_UNITS ? 'km/h' : 'mi/h',
    height: SI_UNITS ? 'm' : 'ft',
    distance: SI_UNITS ? 'km' : 'mi',
    temperature: SI_UNITS ? 'C' : 'F',
    per_min: '/ min',
    percent: '%'
  };
}