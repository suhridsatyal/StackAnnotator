define([
  'jquery',
  'underscore',
  'backbone',
  'views/home',
  'views/question'
], function($, _, Backbone, HomeView, QuestionView){
  var AppRouter = Backbone.Router.extend({
    routes: {
      // Define some URL routes
      '': 'showHome',
      'question': 'showQuestion', //#question

      // Default
      '*actions': 'showHome'
    }
  });

  var initialize = function(){
    var app_router = new AppRouter;

    app_router.on('route:showHome', function(){
      var homeView = new HomeView();
      homeView.render();
    });

    app_router.on('route:showQuestion', function(){
      var questionView = new QuestionView();
      questionView.render();
    });

    Backbone.history.start();
  };

  return {
    initialize: initialize
  };
});
