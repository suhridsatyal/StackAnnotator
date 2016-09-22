define([
  'jquery',
  'underscore',
  'backbone',
  // Models
  '../models/question',
  '../models/answers',
  '../models/annotations',
  // Templates
  'text!../templates/question.html',
  'text!../templates/tooltip_menu.html',
  'text!../templates/annotations.html'
], function($, _, Backbone,
            QuestionModel, AnswerCollection, AnnotationCollection,
            questionTemplate, tooltipTemplate, annotationsTemplate){

  var QuestionView = Backbone.View.extend({
      initialize: function(options) {
          this.options = options || {};
          this.options.selectedText = "";
      },
      el: $('.container'),
      events: {
          'mouseup #answers': 'onHighlight',
          'mousedown #questionView': 'onDeselect',
          'mouseover .annotation_text': 'onAnnotationHover'
      },
      onHighlight: function(){
        var rects = [];
        var selectedText = "";

        if (window.getSelection) {
          selectedText = window.getSelection().toString();
          var box = window.getSelection().getRangeAt(0).getBoundingClientRect();
          rects = this.getHighlightOffset(box);
        } else if (document.selection) {
          selectedText = document.getSelection().toString();
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
      onAnnotationHover:function(evt) {
          debugger;
          var id=evt.target.id;
          // Show annotation
          console.log("Hovered");
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
          self.options = this.options;
          var data = {};

          var question = new QuestionModel({post: this.options.post});
          var answers = new AnswerCollection({post: this.options.post});
          var annotations = new AnnotationCollection();
          $.when(question.fetch(),
                 answers.fetch(),
                 annotations.fetch({data: {'question_id': self.options.post}}))
            .done(function () {
              data.question = question.get("title");
              data.questionBody = question.get("body");
              var annotationList = annotations.toJSON();
              var annotatedAnswers = self.annotateAnswers(answers.toJSON(), annotationList);
              data.answers = self.sortAnswers(annotatedAnswers);

              var compiledTemplate = _.template(questionTemplate);
              self.$el.empty().append(compiledTemplate(data));
              if (self.options.answerID) {
                  // Scroll to answer
                  var answerElem = "#" + self.options.answerID;
                  var answerElemOffset = $(answerElem).offset();
                  $('html,body').animate({scrollTop: answerElemOffset.top}, "fast");

                  if (self.options.highlightType == 'annotation') {
                      // Scroll to annotation
                      var annotationElem = "#" + self.options.highlightID + ".annotation_text";
                      var annotationElemOffset = $(annotationElem).offset();
                      $('html,body').animate({scrollTop: annotationElemOffset.top}, "fast");

                      self.showYoutubeURL(self.options.highlightID, annotations);
                  } else if (self.options.highlightType == 'task') {
                      // Scroll to Task
                      var annotationElem = "#" + self.options.highlightID + ".task_text";
                      var annotationElemOffset = $(annotationElem).offset();
                      $('html,body').animate({scrollTop: annotationElemOffset.top}, "fast");
                      // Show comment box
                      // TODO
                  }
              }
          });
          this.annotations = annotations;
      },
   showYoutubeURL: function(annotationID, annotations){
      // Shows Annotations (Youtube URLS) next to highlighted text
      var annotationElem = "#" + annotationID + ".annotation_text";
      var annotationElemOffset = $(annotationElem).offset();
      annotationElemOffset.bottom = annotationElemOffset.top + $(annotationElem).outerHeight(true);
      annotationElemOffset.right = annotationElemOffset.left + $(annotationElem).outerWidth(true);
      var youtubeURL =  annotations.get(annotationID).
                      get('annotation').
                      replace("watch?v=", "embed/");

      var annotationData = {id: annotationID,
                          annotation: youtubeURL };
      var annotationLinks = _.template(annotationsTemplate)(annotationData);
      $("#annotate-tooltip").popover({
          trigger: 'focus',
          container: 'body',
          placement: 'right',
          content: function() {
              return annotationLinks;
          },
          html: true
      }).popover('show');
      $(".popover").css({top: annotationElemOffset.top, left: annotationElemOffset.right, 'max-width': '640px', transform: ''}).show();
   },
   annotateAnswers: function(answers, annotations){
       // Surrounds annotated text with span, with id=annotation id
       _.each(annotations, function(annotation) {
         _.each(answers, function(answer) {
            if (answer.answer_id == annotation.answer_id) {
              var replacer = function(match, offset) {
                  if (offset==annotation.position) {
                      return "<span class='highlighted annotation_text' id=" + annotation.id + ">" + match + "</span>";
                  } else {
                      return match;
                  }
              }
              answer.body = answer.body.replace(annotation.keyword, replacer);
           }
         });
       });
       return answers;
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
