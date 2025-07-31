document.addEventListener('DOMContentLoaded', function () {
  // === Mobile Menu Toggle ===
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navMenu = document.querySelector('.nav-menu');
  mobileMenuBtn.addEventListener('click', () => navMenu.classList.toggle('active'));

  document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => navMenu.classList.remove('active'));
  });

  // === Smooth Scrolling ===
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });

  // === Heads Section Popups ===
  const leftImage = document.querySelector('.head-card.left .head-image');
  const rightImage = document.querySelector('.head-card.right .head-image');
  const popupRight = document.getElementById('popup-right');
  const popupLeft = document.getElementById('popup-left');

  if (leftImage && popupRight) {
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
  }

  if (rightImage && popupLeft) {
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

  // === Middle Head Tooltip ===
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

  // === About Section Carousel ===
  const carousel = document.querySelector('.about-image.carousel');
  const images = document.querySelectorAll('.carousel-img');

  if (carousel && images.length > 0) {
    let currentIndex = 0;
    const transitionTime = 2500;
    let rotationInterval;

    // Create dots
    const dotsContainer = document.createElement('div');
    dotsContainer.className = 'carousel-nav';
    carousel.appendChild(dotsContainer);

    images.forEach((_, index) => {
      const dot = document.createElement('div');
      dot.className = 'carousel-dot';
      if (index === 0) dot.classList.add('active');
      dot.addEventListener('click', () => goToImage(index));
      dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll('.carousel-dot');

    function goToImage(index) {
      images.forEach(img => img.classList.remove('active'));
      dots.forEach(dot => dot.classList.remove('active'));
      currentIndex = index;
      images[currentIndex].classList.add('active');
      dots[currentIndex].classList.add('active');
    }

    function nextImage() {
      const nextIndex = (currentIndex + 1) % images.length;
      goToImage(nextIndex);
    }

    // Start rotation
    rotationInterval = setInterval(nextImage, transitionTime);

    
  }

  // === Video Section ===
  const video = document.getElementById("csa-video");
  const playBtn = document.getElementById('customPlay');

  if (video && playBtn) {
    playBtn.addEventListener('click', () => {
      video.play();
      playBtn.style.display = 'none';
    });

    video.addEventListener('play', () => playBtn.style.display = 'none');

    video.addEventListener('click', () => {
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    });

    // Autoplay once using IntersectionObserver
    if (!sessionStorage.getItem('videoPlayed')) {
      const observer = new IntersectionObserver(
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              video.muted = false;
              video.play().then(() => {
                sessionStorage.setItem('videoPlayed', 'true');
                observer.unobserve(video);
              }).catch(err => console.warn("Autoplay blocked:", err));
            }
          });
        },
        { threshold: 0.5 }
      );
      observer.observe(video);
    }
  }

});

// for subject toppers 
document.addEventListener('DOMContentLoaded', () => {
  // Switch Year Tabs
  const yearTabs = document.querySelectorAll('.year-tab');
  const yearToppers = document.querySelectorAll('.year-toppers');

  yearTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const year = tab.dataset.year;

      yearTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      yearToppers.forEach(section => {
        section.classList.remove('active');
        if (section.id === `year-${year}`) {
          section.classList.add('active');
        }
      });
    });
  });

  // Modal Viewer
  const modal = document.getElementById('topper-modal');
  const modalImg = document.getElementById('modal-img');
  const closeBtn = modal.querySelector('.close');

  document.querySelectorAll('.topper-year-card').forEach(card => {
    card.addEventListener('click', () => {
      const imgUrl = card.dataset.image;
      modalImg.src = imgUrl;
      modal.style.display = 'flex';
    });
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    modalImg.src = '';
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      modalImg.src = '';
    }
  });
});
