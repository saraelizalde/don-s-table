// Toggle mobile navigation menu when hamburger button is clicked
document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const navWrapper = document.querySelector('.nav-wrapper');

    /**
     * Toggles the 'active' class on the navigation wrapper
     * to show or hide the mobile menu.
     */
    menuToggle.addEventListener('click', function () {
        navWrapper.classList.toggle('active');
    });
});

// Swap logo image depending on screen width
document.addEventListener('DOMContentLoaded', function () {
    /**
     * Updates the logo image based on the window width.
     * - Uses black logo for screens <= 768px
     * - Uses white logo for screens > 768px
     */
    function swapLogoForTablet() {
        const logoImg = document.querySelector('.logo img');
        if (!logoImg) return;

        if (window.innerWidth <= 768) {
            logoImg.src = '/static/images/logo-black.png';
        } else {
            logoImg.src = '/static/images/logo-white.png';
        }
    }

    // Run on page load and whenever the window is resized
    swapLogoForTablet();
    window.addEventListener('resize', swapLogoForTablet);
});
