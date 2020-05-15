var token = localStorage['token'];
$('#searchForm').submit(function(e) {
  e.preventDefault();
  document.getElementById("searchButton").click;
});

function searchFn() {
  var searchInput = document.getElementById('searchInput').value;
  var urlSend = 'http://pi.cs.oswego.edu:12100/search';

  if (searchInput == "" || searchInput == null) {
    $.ajax({
      url: urlSend,
      headers: { 'token': token },
      type: 'GET',
      success: function(json) {
        localStorage.setItem('searchResultsStored', JSON.stringify(json));
        window.location.href = "search.html";
      }
    });
  } else {
    var feedback_data = '{}';
    const dataToSend = JSON.parse(feedback_data);
    dataToSend.searchInput = searchInput;
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,
    success: function(json) {
      localStorage.setItem('searchResultsStored', JSON.stringify(json));
      window.location.href = "search.html";
    }
  });
  }
}

function searchResults(json) {
  var mainContainer = document.getElementById("myData");
  if (json.length == 0) {
    var div = document.createElement("div");
    div.innerHTML =
      '<div class="card_info"><p class="study_title">' + "No studies found based on the search." + '</p></div>';
    mainContainer.appendChild(div);
  }
  for (var i = 0; i < json.length; i++) {
    var div = document.createElement("div");
    div.innerHTML =
      '<div class="card" onclick="myFunction(' + json[i].studyID + ')";"><div class="card_info"><p class="study_title">' + json[i].title + '</p>' +
      '<p class="study_description">' + json[i].purpose + '</p>' +
      '<div class="author"><img class="author_icon" src="assets/school.svg" alt="author icon">' +
      '<p class="author_name">' + json[i].author + '</p>' +
      '</div>' +
      '<div class="university"><img class="university_icon" src="assets/university.svg" alt="university icon">' +
      '<p class="university_name">' + json[i].institution + '</p>' +
      '</div>' + '</div>' + '<p class="credits">' + json[i].costInCredits + ' Credits' + '</p>' +
      '</div>';
    mainContainer.appendChild(div);
  }
}

function categorySelect(category) {
  document.getElementById("cardCategorizationTitle").innerHTML = category + " Studies";
  var feedback_data = '{"category":"' + category + '"}';
  const dataToSend = JSON.parse(feedback_data);
  var urlSend = 'http://pi.cs.oswego.edu:12100/search';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,

    success: function(json) {
      removeCurrentStudies();
      console.log("Category: %j", json);
      searchResults(json);
    },
  });
}

function subCategorySelect(subcategory) {
  document.getElementById("cardCategorizationTitle").innerHTML = subcategory + " Studies";
  var feedback_data = '{"sub_category":"' + subcategory + '"}';
  const dataToSend = JSON.parse(feedback_data);
  var urlSend = 'http://pi.cs.oswego.edu:12100/search';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,

    success: function(json) {
      removeCurrentStudies();
      console.log("Category: %j", json);
      searchResults(json);
    },
  });
}

function removeCurrentStudies() {
  $("#myData").empty();
}
