document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".product-item").forEach(function (item) {
        item.addEventListener("click", function (e) {
            if (e.target.tagName.toLowerCase() === "a"){
                return;
            }
            const link = item.querySelector("a");
            if (link && link.getAttribute("href")) {
                window.location.href = link.getAttribute("href");
            }
        });
    });
});
