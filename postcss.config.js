module.exports = {
  plugins: [
    {
      postcssPlugin: 'custom-transforms',
      Once(root) {
        // Collect all font-face rules
        const fontFaceRules = [];
        root.walkAtRules('font-face', rule => {
          fontFaceRules.push(rule);
        });

        // Wrap non-awesome font-face rules in media query
        // fontFaceRules.forEach(rule => {
        //   const ruleString = rule.toString();
        //   if (!ruleString.includes('awesome')) {
        //     const newRule = `@media(min-width:901px){${ruleString}}`;
        //     rule.replaceWith(newRule);
        //   }
        // });
      },
    },

    require('autoprefixer'),

    require('cssnano')({
      preset: [
        'default',
        {
          discardComments: { removeAll: true },
          normalizeWhitespace: true,
        },
      ],
    }),
  ],
};

module.exports.plugins[0].postcssPlugin = 'custom-transforms';

module.exports.plugins[0].Once = function(root) {
  // Collect font-face rules first
  const fontFaceRules = [];
  root.walkAtRules('font-face', (rule) => {
    fontFaceRules.push(rule);
  });

  // Remove Lato and Roboto Slab font-face declarations safely
  fontFaceRules.forEach(rule => {
    const ruleStr = rule.toString();
    if (ruleStr.includes('Lato') || ruleStr.includes('Roboto Slab')) {
      rule.remove();
    }
  });

  // Add font-display: swap to remaining font-face rules
  // Re-collect font-face rules after removals:
  const remainingFontFaceRules = [];
  root.walkAtRules('font-face', (rule) => {
    remainingFontFaceRules.push(rule);
  });

  remainingFontFaceRules.forEach(rule => {
    let hasDisplay = false;
    rule.walkDecls('font-display', () => {
      hasDisplay = true;
    });
    if (!hasDisplay) {
      rule.prepend('font-display: swap');
    }
  });

  const fontFaceToWrap = [];
  root.walkAtRules('font-face', rule => {
    fontFaceToWrap.push(rule);
  });

  fontFaceToWrap.forEach(rule => {
    const ruleString = rule.toString();
    if (!ruleString.includes('awesome')) {
      const newRule = `@media(min-width:901px){${ruleString}}`;
      rule.replaceWith(newRule);
    }
  });

  // Replace font family references
  root.walkDecls(decl => {
    if (decl.prop.includes('font-family') || decl.prop.includes('font')) {
      decl.value = decl.value.replace(/\bLato\b/g, 'ui-sans-serif');
      decl.value = decl.value.replace(
        /\bRoboto Slab\b/g,
        "Rockwell, 'Rockwell Nova','Roboto Slab','DejaVu Serif','Sitka Small',serif"
      );
    }
  });

  // Update media query breakpoints
  root.walkAtRules('media', rule => {
    if (rule.params === '(min-width: 1200px)') {
      rule.params = '(min-width: 1500px)';
    }
    if (rule.params === '(min-width: 992px)') {
      rule.params = '(min-width: 1192px)';
    }
  });
};
