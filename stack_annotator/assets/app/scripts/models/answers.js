define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, Config){
    var Answers = Backbone.Model.extend({
        //model: Answer,
        url: function() {
            var url = Config.stackoverflow.url_root +
              this.get("post") +
              Config.stackoverflow.answer_query + Config.stackoverflow.key;
            return url;
        }
        ,
        parse: function(response) {
            return response.items;
        }
    });

    return Answers;
});