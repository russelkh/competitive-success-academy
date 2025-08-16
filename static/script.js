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
  


//for video//
document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("csa-video");
  const playPauseBtn = document.getElementById("playPauseBtn");
  const progressBar = document.getElementById("progressBar");
  const progressContainer = document.getElementById("progressContainer");
  const bufferedBar = document.getElementById("bufferedBar");
  const timeDisplay = document.getElementById("timeDisplay");
  const volumeSlider = document.getElementById("volumeSlider");
  const customPlay = document.getElementById("customPlay");

  // Format time in M:SS
  const formatTime = time => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60).toString().padStart(2, "0");
    return `${minutes}:${seconds}`;
  };

  // Update time display and progress bar
  video.addEventListener("timeupdate", () => {
    progressBar.style.width = `${(video.currentTime / video.duration) * 100}%`;
    timeDisplay.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
  });

  // Update buffered amount
  video.addEventListener("progress", () => {
    if (video.buffered.length) {
      const bufferedEnd = video.buffered.end(video.buffered.length - 1);
      bufferedBar.style.width = `${(bufferedEnd / video.duration) * 100}%`;
    }
  });

  // Play / pause toggle
  const togglePlay = () => {
    if (video.paused) {
      video.play();
      playPauseBtn.classList.add("playing");
      customPlay.style.display = "none";
    } else {
      video.pause();
      playPauseBtn.classList.remove("playing");
      customPlay.style.display = "block";
    }
  };

  playPauseBtn.addEventListener("click", togglePlay);
  customPlay.addEventListener("click", togglePlay);
  video.addEventListener("click", togglePlay);

  // Seek on progress click
  progressContainer.addEventListener("click", e => {
    const rect = progressContainer.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    video.currentTime = (clickX / rect.width) * video.duration;
  });

  // Volume control
  volumeSlider.addEventListener("input", () => {
    video.volume = volumeSlider.value;
  });
});




//head//
document.addEventListener("DOMContentLoaded", function () {
  const headCards = document.querySelectorAll(".head-card");

  headCards.forEach(card => {
    const image = card.querySelector(".head-image");
    const tooltip = card.querySelector(".tooltip-popup");
    const isMiddle = card.classList.contains("middle");
    const isLeft = card.classList.contains("left");
    const isRight = card.classList.contains("right");
    const popup = document.getElementById(isLeft ? "popup-left" : (isRight ? "popup-right" : null));

    // --- Desktop Hover (Skip middle) ---
    if (!isMiddle && popup && window.innerWidth > 768) {
      popup.style.transition = "transform 0.3s ease, opacity 0.3s ease";
      popup.style.position = "fixed";
      popup.style.top = "100px";
      popup.style.width = "50vw";
      popup.style.height = "calc(100vh - 100px)";
      popup.style.opacity = "0";
      popup.style.pointerEvents = "none";
      popup.style.zIndex = "2000";
      popup.style.boxShadow = "0 0 20px rgba(0,0,0,0.2)";
      popup.style.overflowY = "auto";

      if (isLeft) {
        popup.style.right = "0";
        popup.style.left = "auto";
        popup.style.transform = "translateX(100%)";
      } else if (isRight) {
        popup.style.left = "0";
        popup.style.right = "auto";
        popup.style.transform = "translateX(-100%)";
      }

      image.addEventListener("mouseenter", () => {
        popup.style.opacity = "1";
        popup.style.pointerEvents = "auto";
        popup.style.transform = "translateX(0)";
      });

      image.addEventListener("mouseleave", () => {
        popup.style.opacity = "0";
        popup.style.pointerEvents = "none";
        popup.style.transform = isLeft ? "translateX(100%)" : "translateX(-100%)";
      });
    }

    // --- Mobile Click (all images) ---
    if (window.innerWidth <= 768) {
      image.addEventListener("click", e => {
        e.stopPropagation();
        // Close all active tooltips/popups first
        document.querySelectorAll(".tooltip-popup.active, .head-popup.active").forEach(el => {
          el.classList.remove("active");
        });

        if (tooltip) tooltip.classList.toggle("active");
        if (popup) popup.classList.toggle("active");
      });
    }
  });

  // Close mobile popups when clicking outside
  if (window.innerWidth <= 768) {
    document.addEventListener("click", () => {
      document.querySelectorAll(".tooltip-popup.active, .head-popup.active").forEach(el => {
        el.classList.remove("active");
      });
    });
  }
});


const hero = document.querySelector('.hero');
const bg = document.querySelector('.hero-background');

const updateParallax = () => {
const rect = hero.getBoundingClientRect();
if (rect.top < window.innerHeight && rect.bottom > 0) {
  let progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
  progress = Math.max(0, Math.min(1, progress));
  const translateY = progress * 40;
  bg.style.transform = `translateY(${translateY}px)`;
}
};

// Run once on load
updateParallax();

// Then on scroll
window.addEventListener('scroll', updateParallax);

