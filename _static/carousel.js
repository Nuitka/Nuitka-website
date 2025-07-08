// TODO: Instead of set display to none here, do it with a class or a directive.

const carousel = () => {
	let activeIndex = 0;
	let interval = null;

	const setActiveTab = (index) => {
		contents.forEach((el, i) => {
			el.style.display = i === index ? "flex" : "none";
		});

		tabs.forEach((tab, i) => {
			tab.classList.toggle("active", i === index);
		});

		const progressBar = moveProgressBar(index);

		progressBar.style.animation = "none";
		progressBar.offsetHeight;
		progressBar.style.animation = "progress 5s linear forwards";

		activeIndex = index;
	};

	const nextTab = () => {
		activeIndex = (activeIndex + 1) % contents.length;
		setActiveTab(activeIndex);
	};

	const startAutoRotate = () => {
		clearInterval(interval);
		interval = setInterval(nextTab, 5000);
	};

	const tabs = document.querySelectorAll(".carousel-tab-top");

	if (tabs.length === 0) {
		return;
	}

	const contents = document.querySelectorAll(".carousel-main");

	if (contents.length === 0) {
		return;
	}

	const createProgressBar = () => {
		const durationContainer = document.createElement("div");
		durationContainer.className = "carousel-duration";

		const progressBar = document.createElement("div");
		progressBar.className = "carousel-progress";

		durationContainer.appendChild(progressBar);
		return { durationContainer, progressBar };
	};

	let currentProgressBar = null;

	const moveProgressBar = (tabIndex) => {
		const activeTab = tabs[tabIndex];

		if (currentProgressBar) {
			currentProgressBar.remove();
		}

		const { durationContainer, progressBar } = createProgressBar();
		currentProgressBar = durationContainer;
		activeTab.appendChild(durationContainer);

		return progressBar;
	};

	contents.forEach((el, i) => {
		el.style.display = i === 0 ? "flex" : "none";
	});

	tabs.forEach((tab, i) => {
		tab.addEventListener("click", () => {
			setActiveTab(i);
			startAutoRotate();
		});
	});

	setActiveTab(0);
	startAutoRotate();
};

document.addEventListener("DOMContentLoaded", carousel());