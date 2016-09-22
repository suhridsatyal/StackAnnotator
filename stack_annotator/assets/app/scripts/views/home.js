define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/home.html',
  // Utils
  '../views/common_utils'
], function($, _, Backbone, homeTemplate, CommonUtils){
  var HomeView = Backbone.View.extend({
      el: $('.container'),
      events: {
          'click #viewButton': 'onSubmitURL',
          'input #urlField': 'onURLChange'
      },
      urlRegex: new RegExp(
                         '^(https?:\/\/)?stackoverflow\.com\/questions\/([0-9]+)(\/[-a-z\d%_.~+]*)*'
                         ),
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
      render: function() {
          var data = {};
          var compiledTemplate = _.template(homeTemplate, data);
          this.$el.empty().append(compiledTemplate);
      }
  });


  return HomeView;
});
