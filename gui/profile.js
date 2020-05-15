var token = localStorage['token'];
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function bookMark(x) {
  /*x.classList.toggle("fa-bookmark");*/
  x.classList.toggle("orange_icon");
}

function getListPendingStudies() {
  var limit = '2';
  $.ajax({
    url: 'http://pi.cs.oswego.edu:12100/getPending?limit=' + limit,
    headers: { 'token': token },
    dataType: 'json',
    success: function(json) {
      console.log("%j", json);
      var content = "";
      for (var i = 0; i < json.length; i++) {
        content +=
          '<a class="study_link" href="review_study.html?study=' + json[i].studyID + '">' +
          '<div class="admin_wrapper">' +
          '<div>' + json[i].title + '</div>' +
          '<div>' + json[i].author + '</div>' +
          '<div>' + json[i].upload_date + '</div>' +
          '<div>Waiting for review</div>' +
          '</div>' +
          '</a>';
      }
      document.getElementById("listPending").innerHTML = content;
    }
  });
}

function getNotifications() {
  var limit = '2';
  $.ajax({
    url: 'http://pi.cs.oswego.edu:12100/getNotifications',
    headers: { 'token': token },
    dataType: 'json',
    success: function(json) {
      console.log("%j", json);
      var content = "";
      for (var i = 0; i < json.length; i++) {
        content +=
          '<a class="study_link">' +
          '<div class="study_wrapper">' +
          '<div>' + json[i].title + '</div>' +
          '<div>' + json[i].timestamp + '</div>';
        content += '<div>' + json[i].body + '</div>';
        content += '</div>' +
          '</a>';
      }
      document.getElementById("notificationsList").innerHTML = content;
    }
  });
}
