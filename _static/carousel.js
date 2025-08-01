const initCarousel = () => {
  const carousel = document.querySelector(".carousel");
  if (!carousel) {
    console.warn("Carousel not found.");
    return;
  }

  const radios = carousel.querySelectorAll(".carousel-radio");
  const labels = carousel.querySelectorAll(".carousel-tab-top");
  const durationBars = carousel.querySelectorAll(".carousel-duration");

  if (radios.length === 0 || labels.length === 0 || durationBars.length === 0) {
    console.warn("Carousel elements not found.");
    return;
  }

  let current = 0;
  let autoplay = true;
  let currentAnimationEndHandler = null;

  const removeAnimationEndListener = () => {
    if (currentAnimationEndHandler) {
      durationBars[current].removeEventListener(
        "animationend",
        currentAnimationEndHandler
      );
      currentAnimationEndHandler = null;
    }
  };

  const addAnimationEndListener = (index) => {
    currentAnimationEndHandler = () => {
      nextSlide();
    };
    durationBars[index].addEventListener(
      "animationend",
      currentAnimationEndHandler
    );
  };

  const resetAnimation = (index) => {
    const bar = durationBars[index];
    bar.style.animation = "none";
    bar.offsetHeight;
    bar.style.animation = "";
  };

  const goTo = (index) => {
    radios[index].checked = true;
    removeAnimationEndListener();
    current = index;
    addAnimationEndListener(current);
    resetAnimation(current);
  };

  const nextSlide = () => {
    if (!autoplay) return;
    const next = (current + 1) % radios.length;
    goTo(next);
  };

  labels.forEach((label, index) => {
    label.addEventListener("click", () => {
      autoplay = false;
      durationBars.forEach((bar) => bar.remove());
      goTo(index);
    });
  });

  goTo(current);
};

window.addEventListener("load", initCarousel);
