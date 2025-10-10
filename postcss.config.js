module.exports = {
	plugins: [
		{
			postcssPlugin: "custom-transforms",
			Once(root) {
				// Collect all font-face rules
				const fontFaceRules = [];
				root.walkAtRules("font-face", (rule) => {
					fontFaceRules.push(rule);
				});

				// Remove Lato and Roboto Slab font-face declarations safely
				fontFaceRules.forEach((rule) => {
					const ruleStr = rule.toString();
					if (ruleStr.includes("Lato") || ruleStr.includes("Roboto Slab")) {
						rule.remove();
					}
				});

				// Add font-display: swap to remaining font-face rules
				// Re-collect font-face rules after removals:
				const remainingFontFaceRules = [];
				root.walkAtRules("font-face", (rule) => {
					remainingFontFaceRules.push(rule);
				});

				remainingFontFaceRules.forEach((rule) => {
					let hasDisplay = false;
					rule.walkDecls("font-display", () => {
						hasDisplay = true;
					});
					if (!hasDisplay) {
						rule.prepend("font-display: swap");
					}
				});

				const fontFaceToWrap = [];
				root.walkAtRules("font-face", (rule) => {
					fontFaceToWrap.push(rule);
				});

				// Replace font family references
				root.walkDecls((decl) => {
					if (decl.prop.includes("font-family") || decl.prop.includes("font")) {
						decl.value = decl.value.replace(/\bLato\b/g, "ui-sans-serif");
						decl.value = decl.value.replace(
							/\bRoboto Slab\b/g,
							"Rockwell, 'Rockwell Nova','Roboto Slab','DejaVu Serif','Sitka Small',serif",
						);
					}
				});

				// Update media query breakpoints
				root.walkAtRules("media", (rule) => {
					if (rule.params === "(min-width: 1200px)") {
						rule.params = "(min-width: 1500px)";
					}
					if (rule.params === "(min-width: 992px)") {
						rule.params = "(min-width: 1192px)";
					}
				});

			root.walkRules((rule) => {
					// Keep rules that contain fa-fw to avoid breaking SVG width, some of these uses fa-fw for width	control
					if (rule.selector.match(/\.fa([srb]?|\-)/) && !rule.selector.includes("fa-fw")) {
							rule.remove();
					}
			});
			},
		},

		require("autoprefixer"),

		require("@fullhuman/postcss-purgecss").default({
			content: ["output/**/*.html"],
			safelist: [
				// Font Awesome classes
				/^fa-/,
				/^fas$/,
				/^far$/,
				/^fab$/,
				/^fa$/,
				// Sphinx Design classes
				/^sd-/,
				// Hub-related classes
				/^hub-/,
				// Classes that might be added by JS
				/^carousel/,
				/^active$/,
				/^current/,
				// Utility classes
				/^highlight/,
				"nuitka-fa",
				"nuitka-fw",
			],
			defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
		}),

		require("cssnano")({
			preset: [
				"default",
				{
					discardComments: { removeAll: true },
					normalizeWhitespace: true,
				},
			],
		}),
	],
};
