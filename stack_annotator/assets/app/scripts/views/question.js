define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/question.html'
], function($, _, Backbone, questionTemplate){
  var QuestionView = Backbone.View.extend({
      el: $('.container'),
      render: function() {
          var data = {};
          var compiledTemplate = _.template(questionTemplate, data);
          this.$el.empty().append(compiledTemplate);
      }
  });
  return QuestionView;
});
