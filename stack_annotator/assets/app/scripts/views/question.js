define([
  'jquery',
  'underscore',
  'backbone',
  // Models
  '../models/question',
  '../models/answers',
  '../models/annotations',
  '../models/task',
  '../models/video',
  // Templates
  'text!../templates/question.html',
  'text!../templates/tooltip_menu.html',
  'text!../templates/annotations.html',
  'text!../templates/commentbox.html',
  // Utils
  '../views/common_utils',
  'config'
], function($, _, Backbone,
  QuestionModel, AnswerCollection, AnnotationCollection, TaskModel, VideoModel,
  questionTemplate, tooltipTemplate, annotationsTemplate, commentboxTemplate,
  CommonUtils, Config) {

  var QuestionView = Backbone.View.extend({
    el: $('.container_load'),
    initialize: function(options) {
      this.options = options || {};
      this.options.selectedText = "";
      this.options.youtubeRegExp = /^https?\:\/\/www\.youtube\.com\/watch\?v\=([\w-]+)(?:&t=(\w+))?$/g;
      this.TASK_TYPE_EXPLANATION = 0;
      this.TASK_TYPE_TUTORIAL = 1;
      this.TASK_TYPE_USAGE = 2;
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

              self._showYoutubeURL(self.options.highlightID, annotations, self.options.answerID, self.options.taskType);
            }
          }
        });
      this.annotations = annotations;
    },

    //
    // Events and Listeners
    //
    events: {
      'mouseup .answer-item': 'onHighlight',
      'mousedown #questionview': 'onDeselect',
      'mouseover annotation': 'onAnnotationHover'
    },

    onHighlight: function() {
      var rects = this._getSelectionRects();
      if (rects==undefined) {
          this._cleanupPopover();
          return;
      }

      var self = this;

      if (this.options.selectedText.length > 0) {
        this._cleanupPopover();

        //show popover
        $("#annotate-tooltip").popover({
          trigger: 'focus',
          container: 'body',
          placement: 'bottom',
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
        $(".arrow").css({"visibility": "hidden"});

        // Attach events to popover buttons.
        /*
        $("#crowdsourceBtn").on("click", function(event) {
          self.onCrowdsourceMenuSelect();
        });
        */
        //requests
        $("#crowdsourceDetailsBtn").on("click", function(event) {
          self.onCrowdsource(self.TASK_TYPE_EXPLANATION); //TODO: remove magic numbers
        });
        $("#crowdsourceTutorialBtn").on("click", function(event) {
          self.onCrowdsource(self.TASK_TYPE_TUTORIAL);
        });
        $("#crowdsourceUsageBtn").on("click", function(event) {
          self.onCrowdsource(self.TASK_TYPE_USAGE);
        });

        $("#commentBtn").on("click", function(event) {
          self.onComment();
        });
      } else {        
        this._cleanupPopover();
      };
    },

    onDeselect: function() {
      this._cleanupPopover();
    },

    onAnnotationHover: function(evt) {
      var answerDiv = $(evt.target).closest("div")
      var answerID = answerDiv.attr("id");
      this._showYoutubeURL(evt.target.id, this.annotations, answerID);
    },

    onCrowdsource: function(task_type) {
      if (task_type === undefined) {
        task_type = this.TASK_TYPE_EXPLANATION;//default val
      }

      var selection = window.getSelection();
      var range = selection.getRangeAt(0);
      var parentDiv = $(range.commonAncestorContainer.parentNode).closest("div");

      //post parameters
      var taskData = {}
      taskData.answer_id = parentDiv.attr("id");
      taskData.question_id = this.options.post;
      taskData.keyword = this.options.selectedText;
      taskData.annotation_url = "stackannotator.com/#question/" + taskData.question_id + "/" + taskData.answer_id;
      taskData.task_type = task_type;

      var task = new TaskModel(taskData);
      var self = this;

      $.when(task.post()).done(function() {
          self._cleanupPopover();
          $('#tweetSuccess').modal('show');
          $('#tweetSuccessButton').on("click", function(){
              location.reload();
          });
      });
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
        placement: 'bottom',
        content: _.template(commentboxTemplate)({displayBackButton: true}),
        html: true
      }).popover('show');
      $(".popover").css({
        top: rects.bottom,
        left: rects.left,
        transform: ''
      }).show();
      $(".arrow").css({"visibility": "hidden"});

      var selection = window.getSelection();
      var range = selection.getRangeAt(0);
      var parentDiv = $(range.commonAncestorContainer.parentNode).closest("div");
      var answerID = parentDiv.attr("id");
      var self = this;

      // Attach event to popover button.
      $("#backToTooltipMenuBtn").on("click", function(event) {
        self.onHighlight();
      });
      this._attachAnnotationSubmissionHandlers(answerID, this.options.selectedText);
    },

    onHelp: function() {
      $('#helpModal').modal('show');
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

    _showYoutubeURL: function(annotationID, annotations, answerID, taskType) {
      // Shows Annotations (Youtube URLS) next to highlighted text
      this._cleanupPopover();
      var annotationElem = "annotation#" + annotationID;
      var annotationElemOffset = $(annotationElem).offset();
      annotationElemOffset.bottom = annotationElemOffset.top + $(annotationElem).outerHeight(true);
      annotationElemOffset.right = annotationElemOffset.left + $(annotationElem).outerWidth(true);

      var youtubeVideos = [];
      var videos = annotations.get(annotationID).get('videos');
      var popoverTemplate;

      var display_data = {};
      var message = "Please Add Youtube Videos";
      if(!isNaN(taskType) && taskType != null){
        var taskType = parseInt(taskType);
        var description;
        if(taskType == this.TASK_TYPE_EXPLANATION){
          description = "Explanation";
          display_data.video_type = this.TASK_TYPE_EXPLANATION;
        } else if (taskType == this.TASK_TYPE_TUTORIAL){
          description = "Tutorial";
          display_data.video_type = this.TASK_TYPE_TUTORIAL;
        } else if (taskType == this.TASK_TYPE_USAGE){
          description = "Usage";
          display_data.video_type = this.TASK_TYPE_USAGE;
        } else {
          description = "Youtube";
        }
        message = "Please Add " + description + " Videos";
      } 
      display_data.message = message;

      if (videos.length > 0) {
        _.each(videos, function(video) {
            var youtubeURL =  "http://youtube.com/embed/" + video.external_id;
            if (video.start_time) {
                youtubeURL = youtubeURL + "&t=" + video.start_time
            }
            video.url = youtubeURL;
            video.score = video.upvotes - video.downvotes;
        });

        display_data.id = annotationID;
        display_data.videos = videos;
        popoverTemplate = _.template(annotationsTemplate)(display_data);
        $("#annotate-tooltip").popover({
          trigger: 'focus', container: 'body', placement: 'right', content: popoverTemplate, html: true
        }).popover('show');

        $(".popover").css({
          top: annotationElemOffset.top, left: annotationElemOffset.right, 'max-width': '640px', 'min-width': '608px', transform: ''
        }).show();

        $(".arrow").css({top: '2%'});

        var self = this;
        // Attach Events
        $(".upvoteBtn").on("click", function(event) {
            self._updateVideoMetaData(event, "upvote");
        });
        $(".downvoteBtn").on("click", function(event) {
            self._updateVideoMetaData(event, "downvote");
        });
        $(".flagBtn").on("click", function(event) {
            self._updateVideoMetaData(event, "flag");
        });

      } else {
        // Show comment box
        popoverTemplate = _.template(commentboxTemplate)(display_data);
        $("#annotate-tooltip").popover({
          trigger: 'focus', container: 'body', placement: 'right', content: popoverTemplate, html: true
        }).popover('show');

        $(".popover").css({
          top: annotationElemOffset.top, left: annotationElemOffset.right, 'max-width': '640px', transform: ''
        }).show();

     }
     // Attach events for video submission
     this._attachVideoSubmissionHandlers(annotationID);
    },

    _annotateAnswers: function(answers, annotations) {
      // Surrounds annotated text with span, with id=annotation id
      var annotationClass;
      _.each(annotations, function(annotation) {
        _.each(answers, function(answer) {
          if (answer.answer_id == annotation.answer_id) {
            if (annotation.videos.length) {
                annotationClass = 'highlighted'
            } else {
                annotationClass = 'soft_highlighted'
            }
            answer.body = answer.body.replace(annotation.keyword,
                                              "<annotation class='"+ annotationClass + "'" +
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
        this.options.selectedText = window.getSelection().toString().trim();
        var box = window.getSelection().getRangeAt(0).getBoundingClientRect();
        return this._getHighlightOffset(box);
      } else if (document.selection) {
        this.options.selectedText = document.getSelection().toString();
        var box = document.getSelection().getRangeAt(0).getBoundingClientRect();
        return this._getHighlightOffset(box);
      } else {
        return;
      }
    },

    _updateVideoMetaData: function(event, updateType) {
      var self = this;

      var videoNode = event.target.closest("div").parentNode;
      var annotationNode = videoNode.parentNode;
      var video = new VideoModel();
      video.set({id: videoNode.id});

      $.when(video.incrementAttr(updateType)).done(function(){
        if (!(updateType==="flag")) {
          // Do not update score on flag action. We can to show
          // "fresh" score here, but unexpected update to score will be confusing for users.
          var oldScore = $(videoNode).find(".videoScore");
          oldScore.html(video.get("upvotes") - video.get("downvotes"));

          // update global data (videos)
          var currentVideos = self.annotations.get(annotationNode.id).get('videos');
          var globalAnnoataionVideo = _.find(currentVideos, function(obj){return (obj.id == videoNode.id);})
          globalAnnoataionVideo.upvotes = video.get("upvotes");
          globalAnnoataionVideo.downvotes = video.get("downvotes");
          globalAnnoataionVideo.flags = video.get("flags");
        }
        var buttonNode = event.target.closest("button");
        $(buttonNode).prop('disabled', true);
      });
    },

    _attachAnnotationSubmissionHandlers: function(answerID, keyword) {
      // Attach events to popover buttons.
      var self=this;
      $("#urlField").on("input", function(event) {
        var urlRegex= self.options.youtubeRegExp;
        CommonUtils.onURLChange("#urlField", urlRegex);
      });

      // Create an annotation with video
      $("#submitButton").on("click", function(event) {
          var youtubeURL =  $("#urlField").val();
          var taskType = parseInt($("input[name=videoDescription]:checked").val());
          if(isNaN(taskType)){
            taskType = parseInt($("input[name=videoDescription]").val());
          }
          var description;
          //This is not strict, the user may insert inappropriate description
          //video reporting should take care of this
          if(taskType == self.TASK_TYPE_EXPLANATION){
            description = "Explanation";
          } else if (taskType == self.TASK_TYPE_TUTORIAL){
            description = "Tutorial";
          } else if (taskType == self.TASK_TYPE_USAGE){
            description = "Usage";
          } else {
            description = "Explanation";
          }

          var youtubeRegex = self.options.youtubeRegExp;
          var videoData = {}
          youtubeURL.replace(youtubeRegex, function (url, external_id, start_time) {
              videoData.external_id = external_id;
              videoData.start_time = start_time;
              return '';
          });
          videoData.annotation_id = answerID;
          videoData.description = description;
          var annotationNode = event.target.closest("div").parentNode;
          var annotationCollection = new AnnotationCollection();
          var newAnnotation = {};
          newAnnotation.question_id = self.options.post;
          newAnnotation.answer_id = answerID;
          newAnnotation.keyword = keyword;
          newAnnotation.videos = JSON.stringify([videoData]);
          $.when(annotationCollection.post(newAnnotation)).done(function() {
              self._cleanupPopover();
              $('#videoAnnotationModal').modal('show');
              $('#videoAnnotationModalButton').on("click", function(){
                  location.reload();
              });
          });
      });
    },

    _attachVideoSubmissionHandlers: function(annotationID) {
      // Attach events to popover buttons.
      var self=this;
      $("#urlField").on("input", function(event) {
        var urlRegex= self.options.youtubeRegExp;
        CommonUtils.onURLChange("#urlField", urlRegex);
      });

      $("#submitButton").on("click", function(event) {
          var youtubeURL =  $("#urlField").val();
          var youtubeRegex = self.options.youtubeRegExp;
          var videoData = {}

          var taskType = parseInt($("input[name=videoDescription]:checked").val());
          if(isNaN(taskType)){
            taskType = parseInt($("input[name=videoDescription]").val());
          }
          console.log("taskType");
          console.log(taskType);
          var description;
          console.log("self.TASK_TYPE_EXPLANATION");
          console.log(self.TASK_TYPE_EXPLANATION);
          //This is not strict, the user may insert inappropriate description  
          //or using the API to add something different but this is handled with reporting annotations
          if(taskType == self.TASK_TYPE_EXPLANATION){
            description = "Explanation";
          } else if (taskType == self.TASK_TYPE_TUTORIAL){
            description = "Tutorial";
          } else if (taskType == self.TASK_TYPE_USAGE){
            description = "Usage";
          } else {
            description = "Explanation";
          }

          youtubeURL.replace(youtubeRegex, function (url, external_id, start_time) {
              videoData.external_id = external_id;
              videoData.start_time = start_time;
              return '';
          });
          videoData.annotation_id = annotationID;
          videoData.description = description;
          var annotationNode = event.target.closest("div").parentNode;
          var video = new VideoModel(videoData);
          $.when(video.post()).done(function() {
              self._cleanupPopover();
              $('#videoAnnotationModal').modal('show');
              $('#videoAnnotationModalButton').on("click", function(){
                  location.reload();
              });
          });
      });
    }

  });

  return QuestionView;
});
