module.exports = {
  plugins: [
    {
      postcssPlugin: 'custom-transforms',
      Once(root) {
        // Handle font-face rules - wrap non-awesome fonts in media query
        root.walkAtRules('font-face', rule => {
          const ruleString = rule.toString();
          if (!ruleString.includes('awesome')) {
            const newRule = `@media(min-width:901px){${ruleString}}`;
            rule.replaceWith(newRule);
          }
        });

        // Remove Lato font-face declarations
        root.walkAtRules('font-face', rule => {
          if (rule.toString().includes('Lato')) {
            rule.remove();
          }
        });

        // Remove Roboto Slab font-face declarations
        root.walkAtRules('font-face', rule => {
          if (rule.toString().includes('Roboto Slab')) {
            rule.remove();
          }
        });

        // Add font-display: swap to remaining font-face rules
        root.walkAtRules('font-face', rule => {
          let hasDisplay = false;
          rule.walkDecls('font-display', () => {
            hasDisplay = true;
          });
          if (!hasDisplay) {
            rule.prepend('font-display: swap');
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
      }
    },

    require('autoprefixer'),

    require('cssnano')({
      preset: ['default', {
        discardComments: {
          removeAll: true
        },
        normalizeWhitespace: true
      }]
    })
  ]
};

module.exports.plugins[0].postcssPlugin = 'custom-transforms';