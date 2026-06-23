const hamburger = document.getElementById("hamburger");

const navLinks = document.getElementById("nav-links");


hamburger.onclick = function(){

    navLinks.classList.toggle("active");

}