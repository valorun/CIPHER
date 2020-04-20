module.exports = {
  env: {
    browser: true,
    es6: true,
    node: false
  },
  extends: [
    'standard'
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'script'
  },
  rules: {
    'semi': ['error', 'always'],
    'space-before-function-paren': ['error', 'never'],
  }
}
