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
            var url = Config.stackannotator.api_url_root + Config.stackannotator.annotations_endpoint;
            return url;
        },

        post: function(data) {
            return $.post(this.url(), data).done(function(resp){
              console.log(resp);
            });
        },

        parse: function(response) {
            return response;
        },

        incrementAttr: function(annotationID, attrType) {
            var self = this;
            var postUrl = Config.stackannotator.api_url_root + Config.stackannotator.annotation_endpoint;
            return $.post(postUrl + '/' + annotationID +'/' + attrType).done(function(data) {
                self.set(data);
            });
        }
    });

    return Annotations;
});