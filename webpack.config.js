'use strict'
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  devtool: (process.env.ENV === 'localdev' ? 'source-map' : 'none'),
  mode: (process.env.ENV === 'localdev' ? 'development' : 'production'),
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
      { test: /\.(png|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
    ]
  },

  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({filename: './foodalert/static/webpack-stats.json'}),
    new VueLoaderPlugin()
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
    modules: ['node_modules'],
  }
}
