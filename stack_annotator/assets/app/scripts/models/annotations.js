define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Annotations = Backbone.Model.extend({
        urlRoot: 'http://stackannotator.com',
        url: function() {
            var url = this.urlRoot + '/api/annotations';
            return url;
        }
        ,
        parse: function(response) {
            return response.items;
        }
    });

    return Annotations;
});