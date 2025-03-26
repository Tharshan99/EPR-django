// Select the WhatsApp icon element
const whatsappFloat = document.querySelector('.whatsapp-float');

// Set initial visibility state
let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
whatsappFloat.style.display = 'none';

///////// header

// Function to check if the hero section is visible
function isHeroSectionVisible() {
  const heroSection = document.getElementById('hero');
  const heroRect = heroSection.getBoundingClientRect();
  return heroRect.bottom > 0 && heroRect.top < window.innerHeight;
}

// Listen for scroll events
window.addEventListener('scroll', () => {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;

  // Show the WhatsApp icon when scrolling up or down, but not in the hero section
  if (!isHeroSectionVisible()) {
    whatsappFloat.style.display = 'none';
  } else {
    whatsappFloat.style.display = 'none';
  }

  // Change navmenu background when scrolling, but keep text color always black
  const navMenu = document.querySelector('.header');
  const navMenuItems = document.querySelectorAll('.navmenu li a');

  if (currentScrollTop > 0) {
    navMenu.style.backgroundColor = 'white';
  } else {
    navMenu.style.backgroundColor = 'transparent';
  }

  // Ensure text color is always black and apply hover effect dynamically
  navMenuItems.forEach(item => {
    item.style.color = 'black'; // Always black

    // Remove previous event listeners to prevent duplication
    item.removeEventListener('mouseenter', hoverEffect);
    item.removeEventListener('mouseleave', resetEffect);

    // Add hover effect dynamically
    item.addEventListener('mouseenter', hoverEffect);
    item.addEventListener('mouseleave', resetEffect);
  });
});

// Function to change color on hover
function hoverEffect(event) {
  event.target.style.color = '#10002B'; // Change to blue on hover
}

// Function to reset color after hover
function resetEffect(event) {
  event.target.style.color = 'black'; // Reset to black after hover
}

// Ensure color behavior applies when the page loads (not just on scroll)
document.addEventListener('DOMContentLoaded', () => {
  const navMenuItems = document.querySelectorAll('.navmenu li a');

  navMenuItems.forEach(item => {
    item.style.color = 'black'; // Set default color

    // Add hover effect dynamically
    item.addEventListener('mouseenter', hoverEffect);
    item.addEventListener('mouseleave', resetEffect);
  });
});

//////////// Cookies start

document.addEventListener("DOMContentLoaded", function () {
  // Check if the cookie consent has already been given
  if (!localStorage.getItem("cookieConsent")) {
    // Show the popup if consent is not set
    const cookiePopup = document.getElementById("cookieConsentPopup");
    cookiePopup.style.display = "block";

    // Add event listeners for buttons
    document.getElementById("acceptAllCookies").addEventListener("click", function () {
      localStorage.setItem("cookieConsent", "accepted");
      cookiePopup.style.display = "none";
    });

    document.getElementById("rejectAllCookies").addEventListener("click", function () {
      localStorage.setItem("cookieConsent", "rejected");
      cookiePopup.style.display = "none";
    });

    document.getElementById("cookieSettings").addEventListener("click", function () {
      alert("Open cookie settings modal (implement this)");
    });
  }
});




//////////// cookies End