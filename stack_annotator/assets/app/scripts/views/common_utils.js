define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone){

  return {

    onURLChange: function(inputSelector, urlRegex) {
      // Performs validation on URL input forms.
      // If URL is valid, submit button is activated.
      // USAGE: structure your HTML template as home and commentbox
      var url = $(inputSelector).val();
      if (!urlRegex.test(url)) {
          // Make Success Indicators invisible
          $('#urlFormGroup').removeClass('has-success');
          $('#submitButton').prop('disabled', true);
          $('#urlSuccessIcon').addClass('hidden');

          // Make Error Indicators visible
          $('#urlFormGroup').addClass('has-error');
          $('#urlHelpBlock').removeClass('hidden');
          $('#urlErrorIcon').removeClass('hidden');
      } else {
          // Make Success Indicators visible
          $('#urlFormGroup').addClass('has-success');
          $('#urlSuccessIcon').removeClass('hidden');
          $('#submitButton').prop('disabled', false);

          // Make Error Indicators invisible
          $('#urlFormGroup').removeClass('has-error');
          $('#urlHelpBlock').addClass('hidden');
          $('#urlErrorIcon').addClass('hidden');
      }
    }
  }
});