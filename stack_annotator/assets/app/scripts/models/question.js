define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, Config){
    var Question = Backbone.Model.extend({
        url: function() {
            var url = Config.stackoverflow.url_root +
              this.get("post") + Config.stackoverflow.question_query;

            if(Config.stackoverflow.key){
              url += '&key=' + Config.stackoverflow.key;
            }

            return url;
       },
        parse: function(response) {
            return response.items[0];
        }
    });
    return Question;
});