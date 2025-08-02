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
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ✅ Working Head Popup Hover Handling

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.head-image').forEach(image => {
    const card = image.closest('.head-card');
    if (!card) return;

    const isLeft = card.classList.contains('left');
    const isRight = card.classList.contains('right');
    const popup = document.getElementById(isLeft ? 'popup-left' : (isRight ? 'popup-right' : ''));

    if (popup) {
      image.addEventListener('mouseenter', () => {
        popup.style.opacity = '1';
        popup.style.pointerEvents = 'auto';
        popup.style.transform = 'translateX(0)';
      });
      image.addEventListener('mouseleave', () => {
        popup.style.opacity = '0';
        popup.style.pointerEvents = 'none';
        popup.style.transform = isLeft ? 'translateX(-100%)' : 'translateX(100%)';
      });
    }
  });

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
});



  // === About Section Carousel ===
  const carousel = document.querySelector('.about-image.carousel');
  const images = document.querySelectorAll('.carousel-img');
  if (carousel && images.length > 0) {
    let currentIndex = 0;
    const transitionTime = 2500;
    let rotationInterval;

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
      video[video.paused ? 'play' : 'pause']();
    });

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

  // === Subject Toppers ===
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

  const modal = document.getElementById('topper-modal');
  const modalImg = document.getElementById('modal-img');
  const closeBtn = modal?.querySelector('.close');

  document.querySelectorAll('.topper-year-card').forEach(card => {
    card.addEventListener('click', () => {
      const imgUrl = card.dataset.image;
      modalImg.src = imgUrl;
      modal.style.display = 'flex';
    });
  });

  closeBtn?.addEventListener('click', () => {
    modal.style.display = 'none';
    modalImg.src = '';
  });

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      modalImg.src = '';
    }
  });
});
