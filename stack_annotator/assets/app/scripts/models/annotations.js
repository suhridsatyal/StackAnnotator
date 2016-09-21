define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Annotations = Backbone.Model.extend({
        urlRoot: '/api/annotations',
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