$(document).ready(function() {

  let modal = window.location.href.substring(window.location.href.indexOf('#'))

  $(modal).modal('show');

});