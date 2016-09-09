/*global require*/
'use strict';

require.config({
  shim: {
    'bootstrap': {deps: ['jquery'], exports: 'bootstrap'}//,
    //'bootstrap/bootstrap-popover': { deps: ['jquery', 'jquery/bootstrap-tooltip'], exports: '$.fn.popover'},
    //'bootstrap/bootstrap-tooltip': { deps: ['jquery'], exports: '$.fn.tooltip'}
  },
  paths: {
    jquery: '../bower_components/jquery/dist/jquery',
    backbone: '../bower_components/backbone/backbone',
    underscore: '../bower_components/lodash/dist/lodash',
    text: '../bower_components/requirejs-text/text',
    backboneValidation: '../bower_components/backbone-validation',
    bootstrap: '../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap.min',
    'bootstrap/popover':    '../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/popover',
    'bootstrap/tooltip':    '../bower_components/bootstrap-sass-official/assets/javascripts/bootstrap/tooltip'
    }

});

require([
  'jquery',
  'underscore',
  'backbone',
  'bootstrap',
  'app'
   //others
], function ($, _, Backbone, Bootstrap, App) {
  App.initialize();
});
