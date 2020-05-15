var token = localStorage['token'];
$(document).ready(function() {
  var params = new URLSearchParams(window.location.search.slice());
  var study_id = params.get('id');
  //Calls the endpoint for the specific study based on the study id and returns it's json data.
  $.ajax({
    url: 'http://pi.cs.oswego.edu:12100/getPreview?study_id=' + study_id,
    headers: { 'token': token },
    dataType: 'json',
    success: function(json) {
      //Constructs the page and checks if it is in the users wishlist
      checkWishlistStatus(study_id);
      checkIsOwned(study_id);
      document.getElementById('costInCredits').innerHTML = "Credits: " + json.costInCredits;
      document.getElementById('author').innerHTML = "Author: " + json.author;
      document.getElementById('abst').innerHTML = json.abstract;
      document.getElementById('duration').innerHTML = "Duration of the study: " + json.duration + " minutes.";
      document.getElementById('institution').innerHTML = "College: " + json.institution;
      document.getElementById('title').innerHTML = json.title;
      document.getElementById('purpose').innerHTML = json.purpose;
      document.getElementById('responses').innerHTML = "No. of responses: " + json.num_responses;
      document.getElementById('stimuli').innerHTML = "No. of stimuli: " + json.num_stimuli;
      document.getElementById('studyidPlaceholder').value = study_id;

      var img = json.images;
      document.getElementById('imagePreview').src = img;

      var categories = "Categories: ";
      for (i = 0; i < json.categories.length; i++) {
        categories += "<button class='pill'>" + json.categories[i] + "</button>";
      }
      document.getElementById('categories').innerHTML = categories;

      var subcategories = "Subcategories: ";
      for (i = 0; i < json.subcategories.length; i++) {
        subcategories += "<button class='pill'>" + json.subcategories[i] + "</button>";
      }
      document.getElementById('subcategories').innerHTML = subcategories;

      var keywords = "Keywords: ";
      for (i = 0; i < json.keywords.length; i++) {
        keywords += "<button class='pill'>" + json.keywords[i] + "</button>";
      }
      document.getElementById('keywords').innerHTML = keywords;
      var stars = "Rating: ";
      for (i = 0; i < json.rating; i++) {
        stars += "<i class='fa fa-star' aria-hidden='true'></i>";
      }
      document.getElementById('stars').innerHTML = stars;
      if (json.randomize) {
        document.getElementById('random').innerHTML = "Randomized the study?: Yes";
      } else {
        document.getElementById('random').innerHTML = "Randomized the study?: No";
      }
      if (json.reviews.length >= 1) {
        var reviews = '<div class="carousel-item active">' +
          '<div class="card">' +
          '<div class="contain">' +
          '<h4><b>' + json.reviews[0].name + '</b></h4>';
        reviews += '<div class="review"><div class="toCenter">'
        for (var i = 0; i < json.reviews[0].rating; i++) {
          reviews += "<i class='fa fa-star' aria-hidden='true'></i>";
        }
        reviews += '</div></div>';
        reviews += "<p>" + json.reviews[0].comment + "</p>"
        reviews += '</div></div></div>';
        for (var i = 1; i < json.reviews.length; i++) {
          reviews += '<div class="carousel-item">' +
            '<div class="card">' +
            '<div class="contain">' +
            '<h4><b>' + json.reviews[i].name + '</b></h4>';
          reviews += '<div class="review"><div class="toCenter">'
          for (var j = 0; j < json.reviews[i].rating; j++) {
            reviews += "<i class='fa fa-star' aria-hidden='true'></i>";
          }
          reviews += '</div></div>';
          reviews += "<p>" + json.reviews[i].comment + "</p>"
          reviews += '</div></div></div>';
        }
        reviews += '<div class="carousel-item">' +
          '<div class="card">' +
          '<div class="contain">' +
          '<h4><b>' + json.reviews[0].name + '</b></h4>';
        reviews += '<div class="review"><div class="toCenter">'
        for (var j = 0; j < json.reviews[0].rating; j++) {
          reviews += "<i class='fa fa-star' aria-hidden='true'></i>";
        }
        reviews += '</div></div>';
        reviews += "<p>" + json.reviews[0].comment + "</p>"
        reviews += '</div></div></div>';
        document.getElementById('reviews').innerHTML = reviews;
      }
    }
  });
});


//Checks to see if this study is on the users wishlist
function checkWishlistStatus(id) {
  var feedback_data = '{}';
  const dataToSend = JSON.parse(feedback_data);
  dataToSend.study_id = id;
  var urlSend = 'http://pi.cs.oswego.edu:12100/isWishlisted';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,

    success: function(data) {
      if (data == true) {
        document.getElementById("wishlistIcon").classList.add("orange_icon");
      }
    },
    error: function(xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }
  });
}

//Checks to see if the user owns the study
function checkIsOwned(id) {
  var feedback_data = '{}';
  const dataToSend = JSON.parse(feedback_data);
  dataToSend.study_id = id;
  var urlSend = 'http://pi.cs.oswego.edu:12100/isOwned';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,

    success: function(data) {
      if (data == true) {
        var button = document.getElementById("buy_button");
        button.innerHTML = "You already own this study"
        button.disabled = true;
      }
    },
    error: function(xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }
  });
}

/* function that toggles the wishlist icon color */
function bookmarkWishList() {
  if (document.getElementById("wishlistIcon").classList.contains("orange_icon")) {
    document.getElementById("wishlistIcon").classList.remove("orange_icon");
    removeFromWishlist();
  } else {
    document.getElementById("wishlistIcon").classList.add("orange_icon");
    sendData();
  }
}



//------------------------- DATA SEND TO SERVER -----------------
function sendData() {
  var feedback_data = '{}';
  const dataToSend = JSON.parse(feedback_data);
  dataToSend.study_id = document.getElementById("studyidPlaceholder").value;
  var urlSend = 'http://pi.cs.oswego.edu:12100/addWishlist';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,

    success: function(data) {
      console.log("Added to wishlist.")
    },
    error: function(xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }

  });

  console.log("%j", urlSend);
}

function removeFromWishlist() {
  var feedback_data = '{}';
  const dataToSend = JSON.parse(feedback_data);
  dataToSend.study_id = document.getElementById("studyidPlaceholder").value;
  var urlSend = 'http://pi.cs.oswego.edu:12100/removeWishlist';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    data: dataToSend,
    success: function(data) {
      console.log("Removed from wishlist.");
    },
    error: function(xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }

  });
}

//Turns on the overlay when a user purchases a study
function buyOverlay() {
  document.getElementById("overlay_buy").style.display = "block";
  var params = new URLSearchParams(window.location.search.slice());
  console.log(params.get('id'));
  var id = params.get('id');
  var urlSend = 'http://pi.cs.oswego.edu:12100/purchase?study_id='+id+'&credits_available=1000';
  $.ajax({
    url: urlSend,
    headers: { 'token': token },
    type: 'GET',
    success: function(data) {
      console.log("Study purchased.")
    },
    error: function(xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }

  });
}

function off() {
  //Removes the overlay so that it isn't displayed
  document.getElementById("overlay_buy").style.display = "none";
  //Redirect to home page
  window.location.href = "home.html";
}
