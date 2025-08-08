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





  document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("csa-video");
    const playBtn = document.getElementById("customPlay");
  
    if (!video || !playBtn) return;
  
    // Play video on button click
    playBtn.addEventListener("click", () => {
      if (video.paused) {
        video.play().catch(err => {
          console.warn("Autoplay blocked:", err);
          // Retry muted if needed
          video.muted = true;
          video.play();
        });
      } else {
        video.pause();
      }
    });
  
    // Toggle play button visibility
    video.addEventListener("play", () => {
      playBtn.style.display = "none";
    });
  
    video.addEventListener("pause", () => {
      playBtn.style.display = "block";
    });
  
    // Also allow clicking video itself
    video.addEventListener("click", () => {
      if (video.paused) {
        video.play().catch(err => {
          video.muted = true;
          video.play();
        });
      } else {
        video.pause();
      }
    });
  });
  

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
