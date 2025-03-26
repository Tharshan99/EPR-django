////////////// Scrroll
// Select the WhatsApp icon element
const whatsappFloat = document.querySelector('.whatsapp-float');

// Set initial visibility state
let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
whatsappFloat.style.display = 'none';

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
    whatsappFloat.style.display = 'block';
  } else {
    whatsappFloat.style.display = 'none';
  }

  // Update the last scroll position
  lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop; // Avoid negative values

  // Change navmenu li color and background when scrolling
  const navMenu = document.querySelector('.header');
  const navMenuItems = document.querySelectorAll('.navmenu li a');
  const letsTalkButton = document.querySelector('.lets-talk-button'); // Select the button

  if (currentScrollTop > 0) {
    navMenu.style.backgroundColor = 'white';
    navMenuItems.forEach(item => {
      item.style.color = '#10002B';

      item.addEventListener('mouseenter', () => {
        item.style.color = '#360065';
      });
      item.addEventListener('mouseleave', () => {
        item.style.color = '#10002B'; // Changed from 'black' to match scroll color
      });
    });

    // Style the button when scrolled
    letsTalkButton.style.color = '#10002B';
    letsTalkButton.style.borderColor = '#10002B';

    letsTalkButton.addEventListener('mouseenter', () => {
      letsTalkButton.style.color = '#360065';
      letsTalkButton.style.borderColor = '#360065';
    });
    letsTalkButton.addEventListener('mouseleave', () => {
      letsTalkButton.style.color = '#10002B';
      letsTalkButton.style.borderColor = '#10002B';
    });
  } else {
    navMenu.style.backgroundColor = 'transparent';
    navMenuItems.forEach(item => {
      item.style.color = '#ffffff';

      item.addEventListener('mouseenter', () => {
        item.style.color = '#10002B';
      });
      item.addEventListener('mouseleave', () => {
        item.style.color = '#ffffff';
      });
    });

    // Style the button when not scrolled
    letsTalkButton.style.color = 'white';
    letsTalkButton.style.borderColor = 'white';

    letsTalkButton.addEventListener('mouseenter', () => {
      letsTalkButton.style.color = '#10002B';
      letsTalkButton.style.borderColor = '#10002B';
    });
    letsTalkButton.addEventListener('mouseleave', () => {
      letsTalkButton.style.color = 'white';
      letsTalkButton.style.borderColor = 'white';
    });
  }
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