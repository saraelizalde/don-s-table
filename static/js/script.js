document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const navWrapper = document.querySelector('.nav-wrapper');

    menuToggle.addEventListener('click', function () {
        navWrapper.classList.toggle('active');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    function swapLogoForTablet() {
        const logoImg = document.querySelector('.logo img');
        if (!logoImg) return;

        if (window.innerWidth <= 768) {
            logoImg.src = '/static/images/logo-black.png';
        } else {
            logoImg.src = '/static/images/logo-white.png';
        }
    }

    // Run on load and resize
    swapLogoForTablet();
    window.addEventListener('resize', swapLogoForTablet);
});
