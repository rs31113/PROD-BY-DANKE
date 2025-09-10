document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");

    requestAnimationFrame(function () {
        container.classList.add("page-visible");
    });
});