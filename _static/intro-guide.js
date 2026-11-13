/* Intro page: tab sets and the command builder.

   Tab sets are written in reST as ".. container:: intro-tabs" holding
   ".. container:: intro-tab" blocks, each starting with a rubric as its
   label. Without JavaScript they simply show one after another. */

const initIntroTabs = () => {
	const platform = (navigator.userAgentData?.platform || navigator.platform || "").toLowerCase();
	const ownSystem = platform.includes("win")
		? "windows"
		: platform.includes("mac")
			? "macos"
			: platform.includes("linux")
				? "linux"
				: null;

	document.querySelectorAll(".intro-tabs").forEach((set, setIndex) => {
		const panels = Array.from(set.children).filter((child) => child.classList.contains("intro-tab"));
		if (panels.length === 0) {
			return;
		}

		const bar = document.createElement("div");
		bar.className = "intro-tabbar";
		bar.setAttribute("role", "tablist");

		const buttons = panels.map((panel, index) => {
			const rubric = panel.querySelector(":scope > .rubric");
			const label = rubric ? rubric.textContent.trim() : `Tab ${index + 1}`;
			if (rubric) {
				rubric.classList.add("intro-tab-label");
			}

			const button = document.createElement("button");
			button.type = "button";
			button.className = "intro-tabbar-button";
			button.textContent = label;
			button.id = `intro-tab-${setIndex}-${index}`;
			button.setAttribute("role", "tab");

			panel.id = panel.id || `intro-panel-${setIndex}-${index}`;
			panel.setAttribute("role", "tabpanel");
			panel.setAttribute("aria-labelledby", button.id);
			button.setAttribute("aria-controls", panel.id);

			bar.appendChild(button);
			return button;
		});

		const select = (selected, focus) => {
			buttons.forEach((button, index) => {
				const active = index === selected;
				button.setAttribute("aria-selected", String(active));
				button.classList.toggle("intro-selected", active);
				button.tabIndex = active ? 0 : -1;
				panels[index].hidden = !active;
			});
			if (focus) {
				buttons[selected].focus();
			}
		};

		buttons.forEach((button, index) => {
			button.addEventListener("click", () => select(index, false));
		});

		bar.addEventListener("keydown", (event) => {
			const current = buttons.indexOf(document.activeElement);
			if (current < 0) {
				return;
			}
			const last = buttons.length - 1;
			const target = {
				ArrowRight: current === last ? 0 : current + 1,
				ArrowLeft: current === 0 ? last : current - 1,
				Home: 0,
				End: last,
			}[event.key];
			if (target !== undefined) {
				event.preventDefault();
				select(target, true);
			}
		});

		set.insertBefore(bar, set.firstChild);
		set.classList.add("intro-tabs-ready");

		// Operating system tabs open on the visitor's system.
		const own = buttons.findIndex((button) => button.textContent.toLowerCase().replace(/\s/g, "") === ownSystem);
		select(own >= 0 ? own : 0, false);
	});
};

const initIntroBuilder = () => {
	const builder = document.getElementById("intro-builder");
	if (!builder) {
		return;
	}

	const form = builder.querySelector(".intro-builder-form");
	const output = builder.querySelector(".intro-builder-cmd");
	const what = builder.querySelector(".intro-builder-what");
	const formatButtons = builder.querySelectorAll(".intro-builder-format button");
	let format = "cli";

	const quote = (value) => (/[\s"']/.test(value) ? `"${value.replace(/"/g, '\\"')}"` : value);

	const code = (text) => {
		const element = document.createElement("code");
		element.textContent = text;
		return element;
	};

	const describe = (mode, base, inBuild) => {
		const where = inBuild ? "build\\" : "";
		const parts = {
			standalone: ["You get the folder ", code(`${where}${base}.dist`), " with ", code(`${base}.exe`), " inside. Copy the whole folder."],
			onefile: ["You get the single file ", code(`${where}${base}.exe`), ". It needs nothing else."],
			app: ["You get ", code(`${where}${base}.exe`), " on Windows and Linux, and the bundle ", code(`${base}.app`), " on macOS."],
			accelerated: ["You get ", code(`${where}${base}.exe`), ", it still uses the Python installed on this machine."],
			module: ["You get ", code(`${where}${base}.cp313-win_amd64.pyd`), " (for Python 3.13), which ", code(`import ${base}`), " loads instead of the source."],
		}[mode];
		if (mode !== "module") {
			parts.push(" On Linux and macOS, executables end in ", code(".bin"), ".");
		}
		what.replaceChildren(...parts);
	};

	const update = () => {
		const data = new FormData(form);
		const mode = data.get("mode");
		const script = (data.get("script") || "").trim() || "your_program.py";
		const base = script.replace(/\\/g, "/").split("/").pop().replace(/\.pyw?$/, "") || "your_program";
		const makesExe = mode !== "module";
		const makesDist = mode === "standalone" || mode === "onefile" || mode === "app";

		// Options that do not apply to the chosen mode are greyed out and ignored.
		builder.querySelectorAll("[data-needs]").forEach((label) => {
			const applies = label.dataset.needs === "exe" ? makesExe : makesDist;
			label.classList.toggle("intro-builder-off", !applies);
			label.querySelectorAll("input, select").forEach((field) => {
				field.disabled = !applies;
			});
		});

		const options = [`--mode=${mode}`];
		const plugin = data.get("plugin");
		if (plugin) {
			options.push(`--enable-plugins=${plugin}`);
		}
		const datadir = (data.get("datadir") || "").trim().replace(/[\\/]+$/, "");
		if (makesDist && datadir) {
			options.push(`--include-data-dir=${quote(`${datadir}=${datadir}`)}`);
		}
		if (makesExe && data.get("noconsole")) {
			options.push("--windows-console-mode=disable");
		}
		const icon = (data.get("icon") || "").trim();
		if (makesExe && icon) {
			options.push(`--windows-icon-from-ico=${quote(icon)}`);
		}
		if (data.get("outdir")) {
			options.push("--output-dir=build");
		}
		if (data.get("clean")) {
			options.push("--remove-output");
		}
		if (data.get("report")) {
			options.push("--report=compilation-report.xml");
		}

		if (format === "cli") {
			output.textContent = `python -m nuitka ${options.join(" ")} ${quote(script)}`;
		} else {
			const lines = options.map((option) => `# nuitka-project: ${option}`);
			lines.push("", `# Put these lines at the top of ${script}, then run:`, `#   python -m nuitka ${quote(script)}`);
			output.textContent = lines.join("\n");
		}

		describe(mode, base, Boolean(data.get("outdir")));
	};

	form.addEventListener("input", update);
	form.addEventListener("change", update);
	form.addEventListener("submit", (event) => event.preventDefault());

	formatButtons.forEach((button) => {
		button.addEventListener("click", () => {
			format = button.dataset.format;
			formatButtons.forEach((other) => {
				other.setAttribute("aria-pressed", String(other === button));
				other.classList.toggle("intro-selected", other === button);
			});
			update();
		});
	});

	update();
};

const initIntroGuide = () => {
	initIntroTabs();
	initIntroBuilder();
};

// The combined site script loads async, the page may already be parsed.
if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", initIntroGuide);
} else {
	initIntroGuide();
}
