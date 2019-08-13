module.exports = {
  'env': {
    'browser': true,
    'commonjs': true,
    'es6': true
  },
  'extends': [
    'eslint:recommended',
    'plugin:vue/essential',
  ],
  'plugins': [
    'vue',
  ],
  'rules': {
    "semi": [2, "always"],
    "vue/max-attributes-per-line": "off",
    "vue/script-indent" : ["error", 2, { "baseIndent": 1 }]
  },
};
