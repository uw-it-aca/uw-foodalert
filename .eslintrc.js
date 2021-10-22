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
    'plugin:node/recommended'
  ],
  'globals': {
    'Atomics': 'readonly',
    'SharedArrayBuffer': 'readonly',
  },
  'parserOptions': {
    'ecmaVersion': 2019,
    'sourceType': 'module',
  },
  'plugins': [
    'vue',
  ],
  'rules': {
    'node/no-unsupported-features/es-syntax': 'off',
    'no-unused-vars': 'off',
    'prefer-regex-literals': 'off',
    'vue/valid-v-slot': ['error', {
      allowModifiers: true,
    }],
  },
};
