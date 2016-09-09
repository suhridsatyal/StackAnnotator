define([
  'jquery',
  'underscore',
  'backbone',
  // Models
  '../models/question',
  '../models/answers',
  // Templates
  'text!../templates/question.html',
  'text!../templates/tooltip_menu.html'
], function($, _, Backbone, QuestionModel, AnswerCollection, questionTemplate, tooltipTemplate){
  var QuestionView = Backbone.View.extend({
      initialize: function(options) {
          this.options = options || {};
          this.options.selectedText = "";
      },
      el: $('.container'),
      events: {
          'mouseup #answers': 'onHighlight',
          'mousedown #answers': 'onDeselect'
      },
      onHighlight: function(evt){
        var rects = [];
        var selectedText = "";
        if (window.getSelection) {
          selectedText = window.getSelection().toString().trim();

          var box = window.getSelection().getRangeAt(0).getBoundingClientRect();
          rects = this.getHighlightOffset(box);
        } else if (document.selection) {
          selectedText = document.getSelection().toString().trim();

          var box = document.getSelection().getRangeAt(0).getBoundingClientRect();
          rects = this.getHighlightOffset(box);
        } else {
          return;
        }
        this.options.selectedText = selectedText;
        var self=this;

        if (selectedText.length > 0) {
          //show popover
          $("#annotate-tooltip").popover({
              trigger: 'focus',
              container: 'body',
              //placement: 'bottom',
              content: function() {
                  return tooltipTemplate;
              },
              html: true
          }).popover('show');
          $(".popover").css({top: rects.bottom, left: rects.left, transform: ''}).show();

          // Attach events to popover buttons.
          // This cannot be done through backbone view because the DOM is created by popover here
          // This is somewhat dirty. But at this stage, it is simple enough.
          // TODO: make this cleaner.
          $("#crowdsourceBtn").on("click", function(event) {self.onCrowdsource()});
          $("#commentBtn").on("click", function(event) {self.onComment()});
          $("#helpBtn").on("click", function(event) {self.onHelp()});
        };
      },
      getHighlightOffset: function(box) {
        /* Returns offset of selected text.
         * Code adapted from this tutorial:
         * http://javascript.info/tutorial/coordinates
         */
        var body = document.body;
        var docElem = document.documentElement;

        var scrollTop = window.pageYOffset || docElem.scrollTop || body.scrollTop;
        var scrollLeft = window.pageXOffset || docElem.scrollLeft || body.scrollLeft;

        var clientTop = docElem.clientTop || body.clientTop || 0;
        var clientLeft = docElem.clientLeft || body.clientLeft || 0;

        var bottom = box.bottom +  scrollTop - clientTop;
        var left = box.left + scrollLeft - clientLeft;
        var right = box.right + scrollLeft - clientLeft;


        return { bottom: Math.round(bottom), left: Math.round(left), right: Math.round(right) };
      },
      onDeselect: function() {
        $("#annotate-tooltip").popover('hide');
      },
      onCrowdsource: function () {
          console.log("TODO: call backend to create crowdsourcing request");
          console.log("Selected Text: " + this.options.selectedText);
      },
      onComment: function () {
          console.log("TODO: allow users to comment");
      },
      onHelp: function () {
          console.log("TODO: show help");
      },
      render: function() {
          var self = this;
          var data = {};

          var question = new QuestionModel({post: this.options.post});
          var answers = new AnswerCollection({post: this.options.post});
          $.when(question.fetch(),answers.fetch())
            .done(function () {
              data.question = question.get("title");
              data.questionBody = question.get("body");
              data.answers = self.sortAnswers(answers.toJSON());
              var compiledTemplate = _.template(questionTemplate);
              self.$el.empty().append(compiledTemplate(data));
          });
      },
   sortAnswers: function(unsortedAnswers) {
        var sortedEntries = [];

        var acceptedAnswer = _.find(unsortedAnswers, function(answer){return answer.is_accepted==true});
        var otherAnswers = _.reject(unsortedAnswers, function(answer){return answer.is_accepted==true});

        if (!(typeof acceptedAnswer == "undefined")) {
            sortedEntries.push(acceptedAnswer);
        };
        var sortedAnswers = sortedEntries.concat(
            _.sortBy(otherAnswers, function(answer) {return -answer.score;}));

        return sortedAnswers;
   }
  });
  return QuestionView;
});
