'use strict'
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  devtool: 'source-map',
  mode: 'development',
  context: __dirname,
  entry: {
      main:  './foodalert/static/foodalert/js/main',
      host: './foodalert/static/foodalert/js/host',
      signup: './foodalert/static/foodalert/js/signup',
      audit: './foodalert/static/foodalert/js/audit',
      base: './foodalert/static/foodalert/js/base',
  },
  output: {
      path: path.resolve('./foodalert/static/foodalert/bundles/'),
      filename: "[name]-[hash].js",
      chunkFilename: '[id]-[chunkhash].js',
      publicPath: '/static/foodalert/bundles/',
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.js?$/,
        loader: 'babel-loader'
      },
      {
        test: /\.(css|scss|less)/,
        use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' },
        ]
      },
      {
        test: /\.(scss)/,
        use: [
            { loader: 'sass-loader'},
        ]
      },
      {
        test: /\.(less)/,
        use: [
            { loader: 'less-loader'},
        ]
      },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
    ]
  },

  plugins: [
    new BundleTracker({filename: './project/webpack-stats.json'}),
    new VueLoaderPlugin()
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
    modules: ['node_modules'],
  }
}
