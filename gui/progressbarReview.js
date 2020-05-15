var currentTab = 0;
showTab(currentTab);
//when button is pushed tab is updated.
/*
function fileFunction() {
  var x = document.createElement("INPUT");
  x.setAttribute("type", "file");
  document.body.appendChild(x);
}
*/

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }


  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    var pb = document.getElementById("nextBtn");
    pb.id = "publishBtn";
    document.getElementById("publishBtn").setAttribute("onClick", "on()");
  } else if(document.getElementById("publishBtn")) {
    document.getElementById("publishBtn").innerHTML = "Next";
    document.getElementById("publishBtn").setAttribute("onClick", "nextPrev(1)");
    var nextToPb = document.getElementById("publishBtn");
    nextToPb.id = "nextBtn";
  }
  //update progress bar
  indicator(n)
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");
  if (n == 1 && !validateForm()) return false;
  x[currentTab].style.display = "none";
  currentTab = currentTab + n;
  if (currentTab >= x.length) {
    document.getElementById("msform").submit();
    return false;
  }
  showTab(currentTab);
}
//Check if section is empty
//can later be redeveloped to check if this is an authenticated user?
function validateForm() {
  var x, y, i, z, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  z = x[currentTab].getElementsByTagName("textarea");
  for (i = 0; i < y.length; i++) {
    if (y[i].value == "") {
      y[i].className += " invalid";
      valid = true;
    }
  }
  for (i = 0; i < z.length; i++) {
    if (z[i].value == "") {
      z[i].className += " invalid";
      valid = true;
    }
  }
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid;
}

//This is for the progressbar
function indicator(n) {
  var x = document.getElementsByClassName("step");
  for (i = x.length - 1; i >= n; i--) {
    x[i].className = x[i].className.replace(" active", "");
  }
  x[n].className += " active";
}
