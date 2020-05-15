function help(){
    var modalImg = document.getElementById("helpImg");
    document.getElementById("helpModal").style.display = "block";
    modalImg.src = "assets/help.png";
}

// When the user clicks on <span> (x), close the modal
function helpClose() {
  document.getElementById("helpModal").style.display = "none";
}
