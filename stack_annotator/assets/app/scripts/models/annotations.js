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
        },
        incrementAttr: function(annotationid, attrType) {
            var self = this;
            var postUrl = settings.stackannotator.api_url_root + settings.stackannotator.annotation_increment_resource_endpoint;
            return $.post(postUrl + '/' + annotationid +'/' + attrType).done(function(data) {
                //self.set(attrType+'s', data[attrType+'s']);
                self.set(data);
            });
        }
    });

    return Annotations;
});