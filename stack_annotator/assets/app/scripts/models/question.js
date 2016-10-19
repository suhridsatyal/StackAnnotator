define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, settings){
    var Question = Backbone.Model.extend({
        url: function() {
            var url = settings.stackoverflow.url_root +
              this.get("post") +
              settings.stackoverflow.question_query + settings.stackoverflow.key;
            return url;
       },
        parse: function(response) {
            return response.items[0];
        }
    });
    return Question;
});