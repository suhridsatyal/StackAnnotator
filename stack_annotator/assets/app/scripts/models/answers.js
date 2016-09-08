define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Answers = Backbone.Model.extend({
        //model: Answer,
        urlRoot: 'https://api.stackexchange.com/2.2/questions/',
        url: function() {
            var url = this.urlRoot +
              this.get("post") +
              '/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody&key=L30zaZ1PnRBr57w8wAxBMQ((';
            return url;
        }
        ,
        parse: function(response) {
            return response.items;
        }
    });

    return Answers;
});