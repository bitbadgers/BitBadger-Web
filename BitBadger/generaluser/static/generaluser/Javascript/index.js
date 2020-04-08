// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal-login) {
        modal-login.style.display == "none";
    }
}
function collapser() {
    var x = document.getElementById("navigate");
    if (x.className === "navbar") {
        document.getElementById("to-cancel").innerHTML = "&times;"
        x.className += "-clicked";
    } else {
        document.getElementById("to-cancel").innerHTML = "&#9776;"
        x.className = "navbar";
    }
}