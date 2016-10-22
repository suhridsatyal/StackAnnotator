define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/home.html',
  // Utils
  '../views/common_utils',
  'config'
], function($, _, Backbone, homeTemplate, CommonUtils, settings){
  var HomeView = Backbone.View.extend({
      el: $('.container_load'),
      events: {
          'click #submitButton': 'onSubmitURL',
          //'click #reportButton': 'onReportAnnotation',
          'keyup #urlField' : 'onKeyPressEvent',
          'keypress #urlField' : 'onKeyPressEvent',
          'input #urlField': 'onURLChange'
      },
      urlRegex: new RegExp(settings.regex.stackoverflow),

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
        if(keyCode == 13){
            this.onSubmitURL(e);
        }
      },
      render: function() {
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
