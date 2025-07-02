window.addEventListener("load", function () {
	const carousels = document.querySelectorAll(".carousel");
	carousels.forEach((carousel) => {
		const radios = carousel.querySelectorAll(".carousel-radio");
		const labels = carousel.querySelectorAll(".carousel-tab-top");

		let current = 0;
		let autoplay = true;
		let timeoutId = null;

		function getDuration(index) {
			const label = labels[index];
			const duration = label?.getAttribute("data-duration");
			return parseInt(duration, 10);
		}

		function goTo(index) {
			radios[index].checked = true;
			current = index;
		}

		function nextSlide() {
			if (!autoplay) return;

			const next = (current + 1) % radios.length;
			goTo(next);
			scheduleNext();
		}

		function scheduleNext() {
			clearTimeout(timeoutId);
			timeoutId = setTimeout(nextSlide, getDuration(current));
		}

		labels.forEach((label, index) => {
			label.addEventListener("click", () => {
				autoplay = false;

				const durationBars = carousel.querySelectorAll(".carousel-duration");

				durationBars.forEach((bar) => bar.remove());

				goTo(index);
				clearTimeout(timeoutId);
			});
		});

		goTo(current);
		scheduleNext();
	});
});
