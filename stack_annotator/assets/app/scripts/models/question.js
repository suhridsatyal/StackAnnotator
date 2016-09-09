define([
  'jquery',
  'underscore',
  'backbone',
], function($, _, Backbone){
    var Question = Backbone.Model.extend({
        urlRoot:'https://api.stackexchange.com/2.2/questions/',
        url: function() {
            var url = this.urlRoot +
              this.get("post") +
              '?order=desc&sort=activity&site=stackoverflow&filter=withbody&key=L30zaZ1PnRBr57w8wAxBMQ(('
            return url;
       },
        parse: function(response) {
            return response.items[0];
        }
    });
    return Question;
});