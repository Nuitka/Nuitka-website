window.addEventListener("load", function () {
  // We will always have a single carousel per page
  const carousel = document.querySelector(".carousel");

  if (!carousel) return;

  const radios = carousel.querySelectorAll(".carousel-radio");
  const labels = carousel.querySelectorAll(".carousel-tab-top");
  const durationBars = carousel.querySelectorAll(".carousel-duration");

  if (radios.length === 0 || labels.length === 0 || durationBars.length === 0)
    return;

  let current = 0;
  let autoplay = true;
  let currentAnimationEndHandler = null;

  function removeAnimationEndListener() {
    if (currentAnimationEndHandler) {
      durationBars[current].removeEventListener(
        "animationend",
        currentAnimationEndHandler
      );
      currentAnimationEndHandler = null;
    }
  }

  function addAnimationEndListener(index) {
    currentAnimationEndHandler = () => {
      nextSlide();
    };
    durationBars[index].addEventListener(
      "animationend",
      currentAnimationEndHandler
    );
  }

  function resetAnimation(index) {
    const bar = durationBars[index];
    bar.style.animation = "none";
    bar.offsetHeight;
    bar.style.animation = "";
  }

  function goTo(index) {
    radios[index].checked = true;

    removeAnimationEndListener();

    current = index;

    addAnimationEndListener(current);

    resetAnimation(current);
  }

  function nextSlide() {
    if (!autoplay) return;

    const next = (current + 1) % radios.length;
    goTo(next);
    scheduleNext();
  }

  labels.forEach((label, index) => {
    label.addEventListener("click", () => {
      autoplay = false;

      durationBars.forEach((bar) => bar.remove());

      goTo(index);
    });
  });

  goTo(current);
});
