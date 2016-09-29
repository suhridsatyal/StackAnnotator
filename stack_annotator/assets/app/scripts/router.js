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
      'question/:post(/:answerID)(/:highlightID)': 'showQuestion', //#question

      // Default
      '*actions': 'showHome'
    }
  });

  var initialize = function(){
    var appRouter = new AppRouter;

    appRouter.on('route:showHome', function(){
      var homeView = new HomeView();
      homeView.render();
    });

    appRouter.on('route:showQuestion', function(post, answerID, highlightID){
      var questionView = new QuestionView({post: post, answerID:answerID,
                                           highlightID:highlightID});
      questionView.render();
    });

    Backbone.history.start();
  };

  return {
    initialize: initialize
  };
});
