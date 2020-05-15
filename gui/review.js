var token = localStorage['token'];
$(document).ready(function() {
  $.ajax({
    url: 'http://pi.cs.oswego.edu:12100/search',
    headers: { 'token': token },
    dataType: 'json',
    success: function(json) {
      document.getElementById('study_title').innerHTML = json[1].title;
      document.getElementById('author_name').innerHTML = "Author: " + json[1].author;
      document.getElementById('study_description').innerHTML = json[1].purpose;
      document.getElementById('university_name').innerHTML = "College: " + json[1].institution;
    }
  });
});
