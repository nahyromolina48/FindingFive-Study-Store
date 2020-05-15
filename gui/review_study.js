var token = localStorage['token'];

//------------------------- IDENTIFY ID of FORM ---------------------------
var id_input = "";

function setInputId(x) {
  window.id_input = x;
}

function getInputId() {
  return window.id_input;
}
//------------------------- INSTRUCTION FORM ---------------------------
function openInstruction() {
  document.getElementById("instruction").style.display = "block";
}

function off_instruction() {
  document.getElementById("instruction").style.display = "none";
}

//------------------------- COMMENT FORM ---------------------------
function changeCheck(x, y) {
  //console.log("changeCheck:"+y);
  x.classList.toggle("fa-times-circle-o");
  x.classList.toggle("orange_close");
  if (document.getElementById(y).innerHTML) {
    openCancelForm(y);
  } else {
    openCommentForm(y);
  }
}

function openCommentForm(y) {
  setInputId(y);
  document.getElementById("comment").style.display = "block";
}

function off_comment() {
  if (!document.getElementById("input-comment").value) {
    document.getElementById("message-comment").innerHTML = "Comment is required";
    return;
  }
  var x = getInputId();
  setInputId("");
  document.getElementById("comment").style.display = "none";
  var comment = document.getElementById("input-comment").value;
  document.getElementById(x).innerHTML = comment;
  document.getElementById("input-comment").value = "";
}

//------------------------- CANCEL FORM ---------------------------
function openCancelForm(y) {
  setInputId(y);
  document.getElementById("cancel").style.display = "block";
}

function off_cancel() {
  var x = getInputId();
  setInputId("");
  document.getElementById(x).innerHTML = "";
  document.getElementById("cancel").style.display = "none";
}

//------------------------- PREVIEW ---------------------------
function updatePreview() {
  var fields_id = ["title_feedback", "reference_feedback", "purpose_feedback", "categories_feedback", "keywords_feedback", "abstract_feedback", "stimuli_feedback", "duration_feedback", "response_feedback", "trials_feedback", "randomized_feedback", "image_videos_feedback", "jsons_feedback"];
  var fields_name = ["Title", "Reference", "Purpose", "Categories", "Keywords", "Abstract", "Stimuli", "Duration", "Response", "Trials", "Randomized", "Images/Videos", "JSON"];
  var preview = "";
  var accept = true;
  for (i = 0; i < fields_id.length; i++) {
    var feedback = document.getElementById(fields_id[i]).innerHTML;
    if (feedback) {
      preview += '<h5 class="fs-subtitle">' + fields_name[i] + ': ' + feedback + '</h5>';
      accept = false;
    }
  }
  if (accept) {
    document.getElementById("preview").innerHTML = '<br><hr><br><h5 class="fs-title">No comments have been made.</h5><h5 class="fs-subtitle">Press <b>Submit</b> to approve the study or <b>Previous</b> to go back and review the study.</h5><hr><br>';
  } else {
    document.getElementById("preview").innerHTML = preview;
  }
}

function nextPrevReview(n) {
  var x = document.getElementsByClassName("tab");
  if (n == 1 && !validateForm()) return false;
  x[currentTab].style.display = "none";
  currentTab = currentTab + n;
  if (currentTab >= x.length) {
    document.getElementById("msform").submit();
    return false;
  }
  showTab(currentTab);
  console.log("Update Preview");
  updatePreview();
}

function getDetailPending(study_id) {
  //var token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODY0ODE3OTUsImV4cCI6MTU5MDgwNTM5NSwic3ViIjoiMTIzNCJ9.bX-XS9h2-8GYocPT8OQgAMK8bNxw41Q0jd6R8Z8S3cs';
  //Get information from server
  $(document).ready(function() {
    $.ajax({
      url: 'http://pi.cs.oswego.edu:12100/getAdminDetails?study_id=' + study_id,
      headers: { 'token': token },
      dataType: 'json',
      success: function(json) {
        console.log("%j", json);
        document.getElementById("title_value").value = json.title;
        document.getElementById("reference_value").value = json.references;
        document.getElementById("purpose_value").value = json.purpose;
        document.getElementById("categories_value").value = json.categories;
        document.getElementById("subcategories_value").value = json.subcategories;

        var keywords = "";
        for (var i = 0; i < json.keywords.length; i++) {
          if (i != 0) {
            keywords += "; ";
          }
          keywords += json.keywords[i];
        }
        document.getElementById("keywords_value").value = keywords;
        document.getElementById("abstract_value").innerHTML = json.abstract;
        document.getElementById("stimuli_value").value = json.num_stimuli;
        document.getElementById("duration_value").value = json.duration;
        document.getElementById("responses_value").value = json.num_responses;
        document.getElementById("trials_value").value = json.num_trials;
        if (json.randomize) {
          document.getElementById("randomized_yes_value").checked = true;
        } else {
          document.getElementById("randomized_no_value").checked = true;
        }

        //View list of images and videos
        var img = json.images;
        var content = ""
        for (i = 0; i < img.length; i++) {
          content += '<div class="preview_img" style="background-image: url(\'' + img[i] + '\')"></div>'
        }
        document.getElementById("images_videos").innerHTML = content;

        //View list of json files
        document.getElementById("json_files").innerHTML = json.template;;
      }
    });
  });
}
