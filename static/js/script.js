/**
 * AI Resume & Cover Letter Generator
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initMobileMenu();
    initCookieConsent();
    initAccordion();
    initApiTest();

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
});

/**
 * Initialize mobile menu functionality
 */
function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }
}

/**
 * Initialize cookie consent banner
 */
function initCookieConsent() {
    const cookieConsent = document.getElementById('cookie-consent');
    const acceptCookiesBtn = document.getElementById('accept-cookies');

    if (cookieConsent && acceptCookiesBtn) {
        // Check if user has already accepted cookies
        if (!localStorage.getItem('cookiesAccepted')) {
            cookieConsent.style.display = 'flex';
        }

        acceptCookiesBtn.addEventListener('click', function() {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieConsent.style.display = 'none';
        });
    }
}

/**
 * Initialize accordion functionality
 */
function initAccordion() {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');

        if (header) {
            header.addEventListener('click', function() {
                item.classList.toggle('active');
            });
        }
    });
}

/**
 * Initialize API test functionality (for demo purposes)
 */
function initApiTest() {
    const getMessageButton = document.getElementById('getMessage');
    const apiMessageDiv = document.getElementById('apiMessage');

    if (getMessageButton && apiMessageDiv) {
        getMessageButton.addEventListener('click', function() {
            // Show loading state
            apiMessageDiv.style.display = 'block';
            apiMessageDiv.textContent = 'Loading...';

            // Fetch message from API
            fetch('/api/hello')
                .then(response => response.json())
                .then(data => {
                    apiMessageDiv.textContent = data.message;
                })
                .catch(error => {
                    apiMessageDiv.textContent = 'Error: ' + error.message;
                });
        });
    }
}
