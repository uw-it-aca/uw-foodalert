'use strict'
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  context: __dirname,
  entry: './foodalert/static/foodalert/js/main',
  output: {
      path: path.resolve('./foodalert/static/foodalert/bundles/'),
      filename: "[name]-[hash].js"
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.(css|scss|less)/,
        use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' },
            { loader: 'sass-loader'},
            { loader: 'less-loader'},
        ]
      },
    ]
  },

  plugins: [
    new BundleTracker({filename: './sampleproj/webpack-stats.json'}),
    new VueLoaderPlugin()
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    modules: ['node_modules'],
  }
}
