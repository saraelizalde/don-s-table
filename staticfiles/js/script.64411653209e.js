/* jshint esversion: 6 */

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

// Reservation cancellation modal
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("cancelModal");
    const closeModalBtn = document.getElementById("closeModal");
    const confirmCancelBtn = document.getElementById("confirmCancel");
    let activeForm = null;

    /**
     * Open the cancellation confirmation modal.
     * Triggered when a "Cancel" button is clicked. Saves a reference
     * to the reservation form that should be submitted if the user confirms.
     */
    document.querySelectorAll(".cancel-btn").forEach(button => {
        button.addEventListener("click", () => {
            activeForm = button.closest("form"); // Save which form was clicked
            modal.style.display = "flex";
        });
    });

    /**
     * Close the modal without submitting the form.
     * Resets the `activeForm` reference to null.
     */
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", () => {
            modal.style.display = "none";
            activeForm = null;
        });
    }

    /**
     * Confirm cancellation.
     * Submits the reservation form associated with the cancel button
     * that was originally clicked.
     */
    if (modal && confirmCancelBtn) {
        confirmCancelBtn.addEventListener("click", () => {
            if (activeForm) activeForm.submit();
        });
    }

    /**
     * Close modal if the user clicks outside the modal content.
     */
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
            activeForm = null;
        }
    });
});