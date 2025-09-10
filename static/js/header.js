function toggleMenu() {
    var menu = document.getElementById("menu");
    var overlay = document.getElementById("overlay");
    if (menu.style.display === "block") {
        menu.style.display = "none";
        overlay.style.display = "none";
        document.body.style.overflow = "";
    } else {
        menu.style.display = "block";
        overlay.style.display = "block";
        document.body.style.overflow = "hidden";
    }
}
