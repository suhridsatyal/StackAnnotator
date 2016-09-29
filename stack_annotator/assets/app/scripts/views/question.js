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
  'text!../templates/annotations.html',
  'text!../templates/commentbox.html',
  // Utils
  '../views/common_utils'
], function($, _, Backbone,
  QuestionModel, AnswerCollection, AnnotationCollection,
  questionTemplate, tooltipTemplate, annotationsTemplate, commentboxTemplate,
  CommonUtils) {

  var QuestionView = Backbone.View.extend({
    el: $('.container'),

    initialize: function(options) {
      this.options = options || {};
      this.options.selectedText = "";
      this.options.youtubeRegExp = new RegExp(
                     '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
                     );
    },

    render: function() {
      var self = this;
      self.options = this.options;
      var data = {};

      var question = new QuestionModel({
        post: this.options.post
      });
      var answers = new AnswerCollection({
        post: this.options.post
      });
      var annotations = new AnnotationCollection();
      $.when(question.fetch(),
          answers.fetch(),
          annotations.fetch({
            data: {
              'question_id': self.options.post
            }
          }))
        .done(function() {
          data.question = question.get("title");
          data.questionBody = question.get("body");
          var annotationList = annotations.toJSON();
          var annotatedAnswers = self._annotateAnswers(answers.toJSON(), annotationList);
          data.answers = self._sortAnswers(annotatedAnswers);

          var compiledTemplate = _.template(questionTemplate);
          self.$el.empty().append(compiledTemplate(data));
          if (self.options.answerID) {
            // Scroll to answer
            var answerElem = "#" + self.options.answerID;
            var answerElemOffset = $(answerElem).offset();
            $('html,body').animate({
              scrollTop: answerElemOffset.top
            }, "fast");

            if (self.options.highlightID) {
              // Scroll to annotation
              var annotationElem = "annotation#" + self.options.highlightID;
              var annotationElemOffset = $(annotationElem).offset();
              $('html,body').animate({
                scrollTop: annotationElemOffset.top
              }, "fast");

              self._showYoutubeURL(self.options.highlightID, annotations);
            }
          }
        });
      this.annotations = annotations;
    },

    //
    // Events and Listeners
    //
    events: {
      'mouseup #answers': 'onHighlight',
      'mousedown #questionview': 'onDeselect',
      'mouseover annotation': 'onAnnotationHover'
    },

    onHighlight: function() {
      var rects = this._getSelectionRects();
      if (rects==undefined) {
          return;
      }

      var self = this;

      if (this.options.selectedText.length > 0) {
        this._cleanupPopover();

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
        $(".popover").css({
          top: rects.bottom,
          left: rects.left,
          transform: ''
        }).show();

        // Attach events to popover buttons.
        $("#crowdsourceBtn").on("click", function(event) {
          self.onCrowdsource();
        });
        $("#commentBtn").on("click", function(event) {
          self.onComment();
        });
        $("#helpBtn").on("click", function(event) {
          self.onHelp();
        });
      };
    },

    onDeselect: function() {
      this._cleanupPopover();
    },

    onAnnotationHover: function(evt) {
      this._showYoutubeURL(evt.target.id, this.annotations);
    },

    onCrowdsource: function() {
      console.log("TODO: call backend to create crowdsourcing request");
      console.log("Selected Text: " + this.options.selectedText);
    },

    onComment: function() {
      this._cleanupPopover();
      var rects=this._getSelectionRects();
      if (rects==undefined) {
          return;
      }
      $("#annotate-tooltip").popover({
        trigger: 'focus',
        container: 'body',
        //placement: 'bottom',
        content: function() {
          return commentboxTemplate;
        },
        html: true
      }).popover('show');
      $(".popover").css({
        top: rects.bottom,
        left: rects.left,
        transform: ''
      }).show();

      var selection = window.getSelection();
      var range = selection.getRangeAt(0);
      var parentDiv = $(range.commonAncestorContainer.parentNode).closest("div");
      var answerID = parentDiv.attr("id");
      var self = this;

      // Attach events to popover buttons.
      $("#urlField.commentbox").on("input", function(event) {
        var urlRegex= self.options.youtubeRegExp;
        CommonUtils.onURLChange("#urlField.commentbox", urlRegex);
      });

      $("#submitButton.commentbox").on("click", function(event) {
          var annotation =  $("#urlField.commentbox").val();
          self.annotations.add({question_id: self.options.post, answer_id: answerID,
                               annotation: annotation});
          //TODO make a POST request
      });

    },

    onHelp: function() {
      console.log("TODO: show help");
    },


    //
    // Helper Functions
    //
    _getHighlightOffset: function(box) {
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

      var bottom = box.bottom + scrollTop - clientTop;
      var left = box.left + scrollLeft - clientLeft;
      var right = box.right + scrollLeft - clientLeft;


      return {
        bottom: Math.round(bottom),
        left: Math.round(left),
        right: Math.round(right)
      };
    },

    _showYoutubeURL: function(annotationID, annotations) {
      // Shows Annotations (Youtube URLS) next to highlighted text
      this._cleanupPopover();
      var annotationElem = "annotation#" + annotationID;
      var annotationElemOffset = $(annotationElem).offset();
      annotationElemOffset.bottom = annotationElemOffset.top + $(annotationElem).outerHeight(true);
      annotationElemOffset.right = annotationElemOffset.left + $(annotationElem).outerWidth(true);

      var youtubeVideos = [];
      var videos = annotations.get(annotationID).get('videos');
      _.each(videos, function(video) {
          var youtubeURL =  "http://youtube.com/embed/" + video.external_id;
          if (video.start_time) {
              youtubeURL = youtubeURL + "&t=" + video.start_time
          }
          video.url = youtubeURL;
          video.score = video.upvotes - video.downvotes;
      });
      var annotationData = {
        id: annotationID,
        videos: videos
      };
      var annotationLinks = _.template(annotationsTemplate)(annotationData);
      console.log(annotationLinks);
      this._cleanupPopover();
      $("#annotate-tooltip").popover({
        trigger: 'focus',
        container: 'body',
        placement: 'right',
        content: annotationLinks,
        //content: function() {
        //  return annotationLinks;
        //},
        html: true
      }).popover('show');

      $(".popover").css({
        top: annotationElemOffset.top,
        left: annotationElemOffset.right,
        'max-width': '640px',
        transform: ''
      }).show();
    },

    _annotateAnswers: function(answers, annotations) {
      // Surrounds annotated text with span, with id=annotation id
      _.each(annotations, function(annotation) {
        _.each(answers, function(answer) {
          if (answer.answer_id == annotation.answer_id) {
            answer.body = answer.body.replace(annotation.keyword,
                                              "<annotation class='highlighted'" +
                                              "id=" + annotation.id + ">" +
                                              annotation.keyword + "</annotation>");
          }
        });
      });
      return answers;
    },

    _sortAnswers: function(unsortedAnswers) {
      var sortedEntries = [];

      var acceptedAnswer = _.find(unsortedAnswers, function(answer) {
        return answer.is_accepted == true;
      });
      var otherAnswers = _.reject(unsortedAnswers, function(answer) {
        return answer.is_accepted == true;
      });

      if (!(typeof acceptedAnswer == "undefined")) {
        sortedEntries.push(acceptedAnswer);
      };
      var sortedAnswers = sortedEntries.concat(
        _.sortBy(otherAnswers, function(answer) {
          return -answer.score;
        }));

      return sortedAnswers;
    },

    _cleanupPopover: function() {
      $(".popover").remove();
      $("#annotate-tooltip").remove();
      $("#questionview").append('<div id="annotate-tooltip" data-toggle="popover"> </div>');
    },

    _getSelectionRects: function() {
      var selectedText;
      if (window.getSelection) {
        this.options.selectedText = window.getSelection().toString();
        var box = window.getSelection().getRangeAt(0).getBoundingClientRect();
        return this._getHighlightOffset(box);
      } else if (document.selection) {
        this.options.selectedText = document.getSelection().toString();
        var box = document.getSelection().getRangeAt(0).getBoundingClientRect();
        return this._getHighlightOffset(box);
      } else {
        return;
      }
    }

  });

  return QuestionView;
});