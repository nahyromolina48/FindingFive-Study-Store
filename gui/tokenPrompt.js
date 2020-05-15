$(document).ready(function() {
  document.getElementById("token_overlay").style.display = "block";
});

function applyToken(token) {

  var urlSend = 'http://pi.cs.oswego.edu:12100/checkToken';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    success: function(json) {
      localStorage['token'] = token;
      localStorage['username'] = json;
      document.getElementById("token_overlay").style.display = "none";
      window.location.href = "home.html";
    }
  });


}
