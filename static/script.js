document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    mobileMenuBtn.addEventListener('click', function () {
      navMenu.classList.toggle('active');
    });
  
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        navMenu.classList.remove('active');
      });
    });
  
    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
        });
      });
      if (window.innerWidth <= 768) {
        const popups = document.querySelectorAll('.head-popup, .tooltip-popup');
        const triggers = document.querySelectorAll('.head-card .head-image');
      
        triggers.forEach(trigger => {
          trigger.addEventListener('click', () => {
            const targetId = trigger.dataset.target;
            const popup = document.getElementById(targetId);
            if (popup) {
              const isVisible = popup.style.opacity === '1';
              popup.style.opacity = isVisible ? '0' : '1';
              popup.style.pointerEvents = isVisible ? 'none' : 'auto';
            }
          });
        });
      
        popups.forEach(popup => {
          popup.addEventListener('click', () => {
            popup.style.opacity = '0';
            popup.style.pointerEvents = 'none';
          });
        });
      }
      
    });
  
    // Carousel
    const images = document.querySelectorAll('.carousel-img');
    let current = 0;
  
    function showImage(index) {
        // Hide all images with smooth fade
        images.forEach(img => {
          img.style.opacity = '0';
          img.classList.remove('active');
        });
        
        // Show new image with smooth fade
        images[index].style.opacity = '1';
        images[index].classList.add('active');
      }
      
      function nextImage() {
        current = (current + 1) % images.length; // Loop automatically
        
        // Special case: When looping back to start
        if (current === 0) {
          // INSTANTLY hide last image
          images[images.length - 1].style.transition = 'none';
          images[images.length - 1].style.opacity = '0';
          
          // Force browser reflow
          void images[0].offsetWidth;
          
          // INSTANTLY show first image (before fade)
          images[0].style.transition = 'none';
          images[0].style.opacity = '1';
          
          // Reset transitions after instant jump
          setTimeout(() => {
            images.forEach(img => {
              img.style.transition = 'opacity 1s ease';
            });
          }, 20);
        } else {
          // Normal smooth transition
          showImage(current);
        }
      }
      
      // Initialize with transition enabled
      images.forEach(img => {
        img.style.transition = 'opacity 1s ease';
      });
      showImage(0);
      
      // Auto-rotate every 3 seconds
      setInterval(nextImage, 3000);
 
  
    // Head Popups
    const leftImage = document.querySelector('.head-card.left .head-image');
    const rightImage = document.querySelector('.head-card.right .head-image');
    const popupRight = document.getElementById('popup-right');
    const popupLeft = document.getElementById('popup-left');
  
    if (leftImage && rightImage && popupRight && popupLeft) {
      leftImage.addEventListener('mouseenter', () => {
        popupRight.style.opacity = '1';
        popupRight.style.pointerEvents = 'auto';
        popupRight.style.transform = 'translateX(0)';
      });
  
      leftImage.addEventListener('mouseleave', () => {
        popupRight.style.opacity = '0';
        popupRight.style.pointerEvents = 'none';
        popupRight.style.transform = 'translateX(100%)';
      });
  
      rightImage.addEventListener('mouseenter', () => {
        popupLeft.style.opacity = '1';
        popupLeft.style.pointerEvents = 'auto';
        popupLeft.style.transform = 'translateX(0)';
      });
  
      rightImage.addEventListener('mouseleave', () => {
        popupLeft.style.opacity = '0';
        popupLeft.style.pointerEvents = 'none';
        popupLeft.style.transform = 'translateX(-100%)';
      });
    }
  
    // Middle Head Tooltip
    const middleImage = document.querySelector('.head-card.middle .head-image');
    const tooltip = middleImage ? middleImage.querySelector('.tooltip-popup') : null;
  
    if (middleImage && tooltip) {
      middleImage.addEventListener('mouseenter', () => {
        tooltip.style.opacity = '1';
        tooltip.style.pointerEvents = 'auto';
      });
  
      middleImage.addEventListener('mouseleave', () => {
        tooltip.style.opacity = '0';
        tooltip.style.pointerEvents = 'none';
      });
    }
  
    // Custom Play Button for Video
    const video = document.getElementById("csa-video");
    const playBtn = document.getElementById('customPlay');
  
    if (video && playBtn) {
      playBtn.addEventListener('click', () => {
        video.play();
        playBtn.style.display = 'none';
      });
  
      video.addEventListener('play', () => {
        playBtn.style.display = 'none';
      });
    }
  
    // Autoplay Video Once with Audio (via sessionStorage)
    if (video && !sessionStorage.getItem('videoPlayed')) {
      const observer = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              video.muted = false;
              video.play()
                .then(() => {
                  sessionStorage.setItem('videoPlayed', 'true');
                  observer.unobserve(video);
                })
                .catch(err => {
                  console.warn("Autoplay blocked by browser:", err);
                });
            }
          });
        },
        { threshold: 0.5 }
      );
  
      observer.observe(video);
    }
    // ✅ Toggle play/pause on click
if (video) {
    video.addEventListener('click', function () {
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    });
  }
  
    // Lazy-load Map
    const mapContainer = document.getElementById('map-container');
    const placeholder = document.getElementById('map-placeholder');
  
    if (mapContainer && placeholder) {
      const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !document.getElementById('lazy-map')) {
            const iframe = document.createElement('iframe');
            iframe.id = 'lazy-map';
            iframe.src = "https://www.google.com/maps/embed?pb=..."; // Replace with real map URL
            iframe.width = "100%";
            iframe.height = "400";
            iframe.style.border = "0";
            iframe.allowFullscreen = true;
            iframe.loading = "lazy";
  
            placeholder.replaceWith(iframe);
            observer.unobserve(mapContainer);
          }
        });
      }, {
        rootMargin: "200px"
      });
  
      observer.observe(mapContainer);
    }
  });
  // Initialize carousel
const images = document.querySelectorAll('.carousel-img');
let current = 0;

function showImage(index) {
  images.forEach(img => img.classList.remove('active'));
  images[index].classList.add('active');
}

// Auto-rotate every 3 seconds
setInterval(() => {
  current = (current + 1) % images.length;
  showImage(current);
}, 3000);

// Start with first image
showImage(0);