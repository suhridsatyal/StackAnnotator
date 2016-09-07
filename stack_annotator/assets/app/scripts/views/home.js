define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/home.html'
], function($, _, Backbone, homeTemplate){
  var HomeView = Backbone.View.extend({
      el: $('.container'),
      events: {
          'click #viewButton': 'onSubmitURL',
          'input #urlField': 'onURLChange'
      },
      urlRegex: new RegExp(
                         '^(https?:\/\/)?stackoverflow\.com\/questions\/([0-9]+)?(\/[-a-z\d%_.~+]*)*'
                         ),
      onURLChange: function(e) {
        e.preventDefault();
        console.log("URL Changed");
        var url = $('#urlField').val();
        if (!this.urlRegex.test(url)) {
            // Make Success Indicators invisible
            $('#urlFormGroup').removeClass('has-success');
            $('#viewButton').prop('disabled', true);
            $('#urlSuccessIcon').addClass('hidden');

            // Make Error Indicators visible
            $('#urlFormGroup').addClass('has-error');
            $('#urlHelpBlock').removeClass('hidden');
            $('#urlErrorIcon').removeClass('hidden');
        } else {
            // Make Success Indicators visible
            $('#urlFormGroup').addClass('has-success');
            $('#urlSuccessIcon').removeClass('hidden');
            $('#viewButton').prop('disabled', false);

            // Make Error Indicators invisible
            $('#urlFormGroup').removeClass('has-error');
            $('#urlHelpBlock').addClass('hidden');
            $('#urlErrorIcon').addClass('hidden');
        }
      },
      onSubmitURL: function(e) {
        e.preventDefault();
        var url = $('#urlField').val();
        var match = this.urlRegex.exec(url);
        console.log(match[2]);
      },
      render: function() {
          var data = {};
          var compiledTemplate = _.template(homeTemplate, data);
          this.$el.empty().append(compiledTemplate);
      }
  });


  return HomeView;
});
