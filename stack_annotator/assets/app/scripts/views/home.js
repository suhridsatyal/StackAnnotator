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
      KEYBOARD_CODE_ENTER: 13,
      el: $('.container_load'),
      events: {
          'click #submitButton': 'onSubmitURL',
          //'click #helpButton': 'onHelp',
          'keyup #urlField' : 'onKeyPressEvent',
          'keypress #urlField' : 'onKeyPressEvent', //we have both events due to possible browser differences
          'input #urlField': 'onURLChange'
      },
      urlRegex: new RegExp('^(https?:\/\/)?stackoverflow\.com\/questions\/([0-9]+)(\/[-a-z\d%_.~+]*)*'),

      onURLChange: function(e) {
        CommonUtils.onURLChange('#urlField', this.urlRegex);
      },
      onSubmitURL: function(e) {
        e.preventDefault();
        var url = $('#urlField').val();
        var match = this.urlRegex.exec(url);
        var nextURL = 'question/' + match[2];
        Backbone.history.navigate(nextURL, true);
      },
      onKeyPressEvent: function(e){
        if(e === null) return

        var keyCode = e.keyCode || e.which;
        if(keyCode == this.KEYBOARD_CODE_ENTER){ 
            this.onSubmitURL(e);
        }
      },
      onHelp: function() {
        console.log("TODO: show help");
        $('#helpModal').modal('show');
      },
      render: function() {
          this._cleanupPopover();
          var data = {};
          var compiledTemplate = _.template(homeTemplate, data);
          //for some reason I cannot attach this to the events
          $("#helpButton").on("click", function(event) {
            self.onHelp();
          });
          this.$el.empty().append(compiledTemplate);
      },
      _cleanupPopover: function() {
        $(".popover").remove();
        $("#annotate-tooltip").remove();
      },
      
  });


  return HomeView;
});
