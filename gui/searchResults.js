var token = localStorage['token'];

$(document).ready(function() {
  $.ajaxSetup({
    headers: { 'token': token }
  });
  var retrievedData = localStorage.getItem('searchResultsStored');
  var data = JSON.parse(retrievedData);
  console.log("LocalStorage JSON: %j", data);
  if (data.length == 0) {
    noStudiesFound();
  }
  for (var i = 0; i < data.length; i++) {
    displayStudyCards(data[i]);
  }
});

function categorySelectSP(category) {
  var feedback_data = '{"category":"' + category + '"}';
  const dataToSend = JSON.parse(feedback_data);
  var urlSend = 'http://pi.cs.oswego.edu:12100/search';
  $.ajax({
    url: urlSend,
    type: 'GET',
    data: dataToSend,

    success: function(json) {
      localStorage.setItem('searchResultsStored', JSON.stringify(json));
      removeCurrentStudies();
      console.log("Category: %j", json);
      searchResults(json);
    },
  });
}

function subCategorySelectSP(subcategory) {
  var feedback_data = '{"sub_category":"' + subcategory + '"}';
  const dataToSend = JSON.parse(feedback_data);
  var urlSend = 'http://pi.cs.oswego.edu:12100/search';
  $.ajax({
    url: urlSend,
    type: 'GET',
    data: dataToSend,

    success: function(json) {
      localStorage.setItem('searchResultsStored', JSON.stringify(json));
      removeCurrentStudies();
      console.log("Category: %j", json);
      searchResults(json);
    },
  });
}

function removeCurrentStudies() {
  $("#myData").empty();
}

function myFunction(id) {
  window.location.href = "preview.html?id=" + id;
}

//Filters the search results based on the users selection.
function filterSearch(field, option) {
  var localTest = localStorage.getItem('searchResultsStored');
  var localRes = JSON.parse(localTest);
  var searchReturnSize = localRes.length;
  removeCurrentStudies();

  if (field == "duration") {
    console.log("option: ", option);
    var minMaxValue = option.split("-");
    var minValue = Number(minMaxValue[0]);
    var maxValue = Number(minMaxValue[1]);
    for (var i = 0; i < searchReturnSize; i++) {
      if (localRes[i].duration <= maxValue && localRes[i].duration >= minValue) {
        console.log("matched study: %j", localRes[i]);
        displayStudyCards(localRes[i]);
      } else {
        console.log("No studies can be found based off of your filter choices.");
      }
    }
  }

  if (field == "price") {
    console.log("option: ", option);
    var minMaxValue = option.split("-");
    var minValue = Number(minMaxValue[0]);
    var maxValue = Number(minMaxValue[1]);
    console.log("Min: " + minValue + "Max: " + maxValue);
    for (var i = 0; i < searchReturnSize; i++) {
      if (localRes[i].costInCredits <= maxValue && localRes[i].costInCredits >= minValue) {
        console.log("matched study: %j", localRes[i]);
        displayStudyCards(localRes[i]);
      } else {
        console.log("No studies can be found based off of your filter choices.");
      }
    }
  }

  if (field == "rating") {
    console.log("option: ", option);
    var ratingSelection = Number(option);
    for (var i = 0; i < searchReturnSize; i++) {
      var studyRating = Number(localRes[i].rating);
      if (studyRating == option) {
        console.log("matched study: %j", localRes[i]);
        displayStudyCards(localRes[i]);
      } else {
        console.log("No studies can be found based off of your filter choices.");
      }
    }
  }

  if (field == "uploaddate") {
    console.log("option: ", option);

    var dateRange = option;

    for (var i = 0; i < searchReturnSize; i++) {
      //Retrieve time from study, convert it to MM-DD-YYYY format
      var studyDate = new Date(localRes[i].upload_date).getTime();
      var studyDateFormatted = moment.utc(studyDate).format('MM-DD-YYYY');

      //Convert todays date and a month previous from todays date to MM-DD-YYYY format
      var todaysDate = moment().format('MM-DD-YYYY');
      var dateFrom = moment().subtract(dateRange, 'days');
      var oneMonthAgo = dateFrom.format('MM-DD-YYYY');

      //See if study is in between todays date and 7 days/a month/6 months/a year ago
      if (moment(studyDateFormatted).isAfter(oneMonthAgo) && moment(studyDateFormatted).isBefore(todaysDate)) {
        console.log("matched study: %j", localRes[i]);
        displayStudyCards(localRes[i]);
      } else {
        console.log("No studies can be found based off of your filter choices.");
      }
    }
  }

}

function displayStudyCards(data) {
  var mainContainer = document.getElementById("myData");
  var div = document.createElement("div");
  div.innerHTML =
    '<div class="card" onclick="myFunction(' + data.studyID + ')";"><div class="card_info"><p class="study_title">' + data.title + '</p>' +
    '<p class="study_description">' + data.purpose + '</p>' +
    '<div class="author"><img class="author_icon" src="assets/school.svg" alt="author icon">' +
    '<p class="author_name">' + data.author + '</p>' +
    '</div>' +
    '<div class="university"><img class="university_icon" src="assets/university.svg" alt="university icon">' +
    '<p class="university_name">' + data.institution + '</p>' +
    '</div>' + '</div>' + '<p class="credits">' + data.costInCredits + ' Credits' + '</p>' +
    '</div>';
  mainContainer.appendChild(div);
}

function noStudiesFound() {
  var mainContainer = document.getElementById("myData");
  var div = document.createElement("div");
  div.innerHTML =
    '<div><p class="filterText">' + "No studies found for this category." + '</p></div>';
  mainContainer.appendChild(div);
}

function getDates(startDate, stopDate) {
  var currentDate = startDate;
  while (currentDate <= stopDate) {
    currentDate = currentDate.addDays(1);
  }
}

/*
function displayAppliedFilter(value) {
  if (value == null) {
  if (!document.getElementById("applyFilterText")) {
    var displayContainer = document.getElementById("filterDisplay");
    var displayFilterDiv = document.createElement("div");
    displayFilterDiv.innerHTML =
    '<ul class="filter" id="displayFilters"><li><p class="filterText" id="applyFilterText"> Applied filter: </p></li></ul><hr><br>';
    displayContainer.appendChild(displayFilterDiv);
  }
}
  if(!document.getElementById("ratingFilterDisplay") {
    var displayContainer = document.getElementById("displayFilters");
    var displayFilterOption = document.createElement("li");
    displayFilterOption.innerHTML =
    '<p class="filterText" id="ratingFilterText">  </p></li></ul><hr><br>';
    displayContainer.appendChild(displayFilterDiv);
  }
}
*/
