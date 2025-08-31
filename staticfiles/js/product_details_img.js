document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("main-image");
    const thumbnails = document.querySelectorAll(".thumbnail");
    const btnLeft = document.querySelector(".thumb-nav.left");
    const btnRight = document.querySelector(".thumb-nav.right");
    const thumbnailsContainer = document.querySelector(".thumbnails-container")

    let currentIndex = 0;

    // change the main img when clicked
    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", () => {
            mainImage.src = thumb.dataset.full;

            thumbnails.forEach(t => t.classList.remove("active"));
            thumb.classList.add("active");

            currentIndex = index;
        });
    });

    // left and right scroll
    btnLeft.addEventListener("click", () => {
        if (currentIndex > 0) {
            currentIndex--;
            thumbnails[currentIndex].click();
            thumbnailsContainer.scrollTo({
                left: thumbnails[currentIndex].offsetLeft - thumbnailsContainer.offsetLeft,
                behavior: "smooth"
            });
        }
    });

    btnRight.addEventListener("click", () => {
        if (currentIndex < thumbnails.length - 1) {
            currentIndex++;
            thumbnails[currentIndex].click();
            thumbnailsContainer.scrollTo({
                left: thumbnails[currentIndex].offsetLeft - thumbnailsContainer.offsetLeft,
                behavior: "smooth"
            });
        }
    });

    // first img active by default
    if (thumbnails.length > 0) {
        thumbnails[0].classList.add("active");
    }
});
