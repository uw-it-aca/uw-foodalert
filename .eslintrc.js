module.exports = {
  'env': {
    'browser': true,
    'commonjs': true,
    'es6': true,
  },
  'extends': [
    'plugin:vue/essential',
    'google',
    'plugin:vue-a11y/recommended',
  ],
  'globals': {
    'Atomics': 'readonly',
    'SharedArrayBuffer': 'readonly',
  },
  'parserOptions': {
    'ecmaVersion': 2018,
  },
  'plugins': [
    'vue',
    'vue-a11y',
  ],
  'rules': {
  },
};
