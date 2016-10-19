define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, settings){
    var Annotation = Backbone.Model.extend({
        idAttribute: "id"
    });

    var Annotations = Backbone.Collection.extend({
        model: Annotation,
        url: function() {
            var url = settings.stackannotator.api_url_root + settings.stackannotator.annotation_post_endpoint;
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