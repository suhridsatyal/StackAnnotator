define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, settings){
    var Answers = Backbone.Model.extend({
        //model: Answer,
        url: function() {
            var url = settings.stackoverflow.url_root +
              this.get("post") +
              settings.stackoverflow.answer_query + settings.stackoverflow.key;
            return url;
        }
        ,
        parse: function(response) {
            return response.items;
        }
    });

    return Answers;
});