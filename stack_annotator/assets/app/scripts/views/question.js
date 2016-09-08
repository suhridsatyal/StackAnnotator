define([
  'jquery',
  'underscore',
  'backbone',
  // Models
  '../models/question',
  '../models/answers',
  // Templates
  'text!../templates/question.html'
], function($, _, Backbone, QuestionModel, AnswerCollection, questionTemplate){
  var QuestionView = Backbone.View.extend({
      initialize: function(options) {
          this.options = options || {};
      },
      el: $('.container'),
      render: function() {
          var self = this;
          self.questionTemplate = questionTemplate;
          var data = {};
          console.log(this.options.post);

          var question = new QuestionModel({post: this.options.post});
          var answers = new AnswerCollection({post: this.options.post});
          $.when(question.fetch(),answers.fetch())
            .done(function () {
              data.question = question.get("title");
              data.questionBody = question.get("body");
              data.answers = answers.toJSON();
              console.log(data);
              var compiledTemplate = _.template(self.questionTemplate);
              self.$el.empty().append(compiledTemplate(data));
          });

      }
  });
  return QuestionView;
});
