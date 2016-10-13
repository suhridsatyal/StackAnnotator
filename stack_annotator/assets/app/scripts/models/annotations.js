define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Annotation = Backbone.Model.extend({
        idAttribute: "id"
    });

    var Annotations = Backbone.Collection.extend({
        model: Annotation,
        urlRoot: 'http://stackannotator.com',
        url: function() {
            var url = this.urlRoot + '/api/annotations';
            return url;
        },
        post: function(data) {
            console.log(data);
            return $.post(this.url(), data).done(function(resp){
                   console.log(resp);
            });
        },
        parse: function(response) {
            return response;
        }
    });

    return Annotations;
});