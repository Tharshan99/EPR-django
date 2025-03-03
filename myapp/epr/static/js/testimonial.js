document.addEventListener("DOMContentLoaded", function () {
    const swiper = new Swiper(".slider-wrapper", {
        slidesPerView: 3,
        spaceBetween: 16,
        centeredSlides: false,
        loop: true, // Enables infinite scrolling
        speed: 2000,
        autoplay: {
            delay: 3000, // Moves one slide every 3 seconds
            disableOnInteraction: false, // Ensures autoplay continues after user interaction
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            320: { slidesPerView: 1, spaceBetween: 8 },
            768: { slidesPerView: 2, spaceBetween: 12 },
            1024: { slidesPerView: 3, spaceBetween: 16 },
        },
        on: {
            init: function () {
                checkNavigationButtons(this);
            },
            slideChange: function () {
                checkNavigationButtons(this);
            },
        },
    });

    function checkNavigationButtons(swiperInstance) {
        const prevButton = document.querySelector(".swiper-button-prev");
        const nextButton = document.querySelector(".swiper-button-next");

        if (swiperInstance.slides.length <= swiperInstance.params.slidesPerView) {
            // Hide navigation buttons if slides are less than visible slides
            prevButton.style.display = "none";
            nextButton.style.display = "none";
        } else {
            prevButton.style.display = "block";
            nextButton.style.display = "block";
        }
    }
});
