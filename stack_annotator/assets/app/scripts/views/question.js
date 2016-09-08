define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/question.html'
], function($, _, Backbone, questionTemplate){
  var QuestionView = Backbone.View.extend({
      initialize: function(options) {
          this.options = options || {};
      },
      el: $('.container'),
      render: function() {
          console.log(this.options);
          var data = {};
          var compiledTemplate = _.template(questionTemplate, data);
          this.$el.empty().append(compiledTemplate);
      }
  });
  return QuestionView;
});
