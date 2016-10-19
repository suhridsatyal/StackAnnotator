
define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, settings){
    var Video = Backbone.Model.extend({
        idAttribute: "id",
        post: function() {
            var self = this;
            var postUrl = settings.stackannotator.api_url_root + settings.stackannotator.video_post_endpoint;
            return $.post(postUrl, self.attributes).done(
              function(data){
                 console.log(data);
              }
            );
        },
        incrementAttr: function(attrType) {
            var self = this;
            var postUrl = settings.stackannotator.api_url_root + settings.stackannotator.video_increment_resource_endpoint;
            return $.post(postUrl + '/' + this.id +'/' + attrType).done(function(data) {
                //self.set(attrType+'s', data[attrType+'s']);
                self.set(data);
            });
        }
    });
    return Video;
});