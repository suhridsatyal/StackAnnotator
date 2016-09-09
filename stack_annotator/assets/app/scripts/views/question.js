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

          var question = new QuestionModel({post: this.options.post});
          var answers = new AnswerCollection({post: this.options.post});
          $.when(question.fetch(),answers.fetch())
            .done(function () {
              data.question = question.get("title");
              data.questionBody = question.get("body");
              data.answers = self.sortAnswers(answers.toJSON());
              console.log(data);
              var compiledTemplate = _.template(self.questionTemplate);
              self.$el.empty().append(compiledTemplate(data));
          });
      },
   sortAnswers: function(unsortedAnswers) {
        var sortedEntries = [];

        var acceptedAnswer = _.find(unsortedAnswers, function(answer){return answer.is_accepted==true});
        var otherAnswers = _.reject(unsortedAnswers, function(answer){return answer.is_accepted==true});

        sortedEntries.push(acceptedAnswer);
        var sortedAnswers = sortedEntries.concat(
            _.sortBy(otherAnswers, function(answer) {return -answer.score;}));

        return sortedAnswers;
   }
  });
  return QuestionView;
});
