const parseTabsData = (elements) => {
	let currentTab = {};
	const tabsData = [];

	elements.forEach((el) => {
		if (el.classList.contains("tab-start")) currentTab = {};
		if (el.classList.contains("tab-label-top"))
			currentTab.labelTop = el.textContent.trim();
		if (el.classList.contains("tab-label-side"))
			currentTab.labelSide = el.textContent.trim();
		if (el.classList.contains("carousel-heading"))
			currentTab.heading = el.textContent.trim();
		if (el.classList.contains("carousel-text"))
			currentTab.text = el.textContent.trim();
		if (el.classList.contains("carousel-button"))
			currentTab.button = el.textContent.trim();
		if (el.classList.contains("tab-end")) tabsData.push({ ...currentTab });
		if (el.classList.contains("cta-link"))
			currentTab.ctaLink = el.textContent.trim();
	});

	return tabsData;
};

const createCarouselTop = () => {
	const carouselTop = document.createElement("div");
	carouselTop.className = "carousel-top";

	const tabsTop = document.createElement("div");
	tabsTop.className = "carousel-tabs-top";

	const carouselDuration = document.createElement("div");
	carouselDuration.className = "carousel-duration";

	const carouselProgress = document.createElement("div");
	carouselProgress.className = "carousel-progress";

	carouselDuration.appendChild(carouselProgress);
	carouselTop.appendChild(tabsTop);
	carouselTop.appendChild(carouselDuration);

	return { carouselTop, tabsTop, carouselProgress };
};

const createCarouselContent = () => {
	const carouselContent = document.createElement("div");
	carouselContent.className = "carousel-content";

	const mainContent = document.createElement("div");
	mainContent.className = "carousel-main";

	const tabsContainer = document.createElement("div");
	tabsContainer.className = "carousel-tabs-side";

	return { carouselContent, mainContent, tabsContainer };
};

const structureCarousel = () => {
 const container = document.querySelector(".carousel-rst-container");
  const elements = Array.from(container.querySelectorAll("p"));
	const tabsData = parseTabsData(elements);

	const carousel = document.createElement("div");
	carousel.className = "carousel";

	const { carouselTop, tabsTop, carouselProgress } = createCarouselTop();
	const { carouselContent, mainContent, tabsContainer } =
		createCarouselContent();

	let activeIndex = 0;
	let interval = null;

	const setActiveTab = (index) => {
		const tab = tabsData[index];

		mainContent.classList.add("fade-out");

		setTimeout(() => {
			mainContent.innerHTML = `
				<h2 class="carousel-heading">${tab.heading}</h2>
				<p class="carousel-text">${tab.text}</p>
				<a class="carousel-button" href="${tab.ctaLink}" target="_blank">
					${tab.button}
					<div class="hub-circle-button">
						<i class="fa fa-arrow-circle-right" aria-hidden="true" style="font-size: 25px;"></i>
					</div>
				</a>
`;

			[...tabsTop.children].forEach((el, i) => {
				el.classList.toggle("active", i === index);
			});

			carouselProgress.style.animation = "none";
			carouselProgress.offsetHeight;
			carouselProgress.style.animation = "progress 5s linear forwards";

			mainContent.classList.remove("fade-out");
			mainContent.classList.add("fade-in");

			setTimeout(() => {
				mainContent.classList.remove("fade-in");
			}, 400);
		}, 400);

		activeIndex = index;
	};

	const nextTab = () => {
		activeIndex = (activeIndex + 1) % tabsData.length;
		setActiveTab(activeIndex);
	};

	const startAutoRotate = () => {
		clearInterval(interval);
		interval = setInterval(nextTab, 5000);
	};

	const createTopTabs = () => {
		tabsData.forEach((tab, index) => {
			const tabDiv = document.createElement("div");
			tabDiv.className = "carousel-tab-top";
			tabDiv.textContent = tab.labelTop || tab.heading;
			tabDiv.addEventListener("click", () => {
				setActiveTab(index);
				startAutoRotate();
			});
			tabsTop.appendChild(tabDiv);
		});
	};

	const createSideTabs = () => {
		tabsData.forEach((tab, index) => {
			const tabDiv = document.createElement("div");
			tabDiv.className = "carousel-tab-side";
			tabDiv.innerHTML = `
				<div class="tab-heading">${tab.labelSide || tab.heading}</div>
				<div class="hub-circle-button">
					<i class="fa fa-arrow-circle-right" aria-hidden="true" style="font-size: 25px;"></i>
				</div>
			`;
			tabDiv.addEventListener("click", () => {
				setActiveTab(index);
				startAutoRotate();
			});
			tabsContainer.appendChild(tabDiv);
		});
	};

	createTopTabs();
	createSideTabs();
	setActiveTab(0);
	startAutoRotate();

	carouselContent.appendChild(mainContent);
	carouselContent.appendChild(tabsContainer);
	carousel.appendChild(carouselTop);
	carousel.appendChild(carouselContent);

	container.innerHTML = ""
	container.appendChild(carousel);
};

structureCarousel();
