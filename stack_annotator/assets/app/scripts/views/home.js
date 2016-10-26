define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/home.html',
  // Utils
  '../views/common_utils',
  'config'
], function($, _, Backbone, homeTemplate, CommonUtils, Config){
  var HomeView = Backbone.View.extend({
      /* View for the landing page */

      KEYBOARD_CODE_ENTER: 13,

      el: $('.container_load'),

      events: {
          'click #submitButton': 'onSubmitURL',
          'input #urlField': 'onURLChange',
          'keyup #urlField' : 'onKeyPressEvent',
          'keypress #urlField' : 'onKeyPressEvent'
      },

      urlRegex: new RegExp('^(https?:\/\/)?stackoverflow\.com\/questions\/([0-9]+)(\/[-a-z\d%_.~+]*)*'),

      onURLChange: function(e) {
        /* Checks validity of URL*/
        CommonUtils.onURLChange('#urlField', this.urlRegex);
      },

      onSubmitURL: function(e) {
        /* Navigate to Question View */
        e.preventDefault();
        var url = $('#urlField').val();
        var match = this.urlRegex.exec(url);
        var nextURL = 'question/' + match[2];
        Backbone.history.navigate(nextURL, true);
      },

      onKeyPressEvent: function(e){
        /* Submit URL if user pressed ENTER instead of clicking button */
        if(e === null){
            return
        }
        var keyCode = e.keyCode || e.which;
        if(keyCode == this.KEYBOARD_CODE_ENTER){
            this.onSubmitURL(e);
        }
      },

      onHelp: function() {
        $('#helpModal').modal('show');
      },

      render: function() {
          /* Renders the view */

          // Cleanup dirty popovers
          // Dirty popovers can exist if user navigates from question view
          this._cleanupPopover();

          var data = {};
          var compiledTemplate = _.template(homeTemplate, data);
          this.$el.empty().append(compiledTemplate);
      },

      _cleanupPopover: function() {
        $(".popover").remove();
        $("#annotate-tooltip").remove();
      },
  });


  return HomeView;
});
