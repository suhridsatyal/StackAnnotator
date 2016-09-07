/*global require*/
'use strict';

require.config({
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    }
  },
  paths: {
    jquery: '../bower_components/jquery/dist/jquery',
    backbone: '../bower_components/backbone/backbone',
    underscore: '../bower_components/lodash/dist/lodash',
    text: '../bower_components/requirejs-text/text',
    bootstrap: '../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap'  }
});

require([
  'jquery',
  'underscore',
  'backbone',
  'app'
], function ($, _, Backbone, App) {
  App.initialize();
});
