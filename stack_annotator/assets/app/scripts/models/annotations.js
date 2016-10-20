define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, Config){
    var Annotation = Backbone.Model.extend({
        idAttribute: "id"
    });

    var Annotations = Backbone.Collection.extend({
        model: Annotation,
        url: function() {
            var url = Config.stackannotator.api_url_root + Config.stackannotator.annotation_post_endpoint;
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