define([
  'jquery',
  'underscore',
  'backbone',
  'config'
], function($, _, Backbone, Config){
    var Task = Backbone.Model.extend({
        idAttribute: "id",
        
        post: function() {
            var self = this;
            var postUrl = Config.stackannotator.api_url_root + Config.stackannotator.task_post_endpoint;
            return $.post(postUrl, self.attributes).done(
                    function(data){
                        console.log(data);
                    }).fail(
                    function(jqXHR, textStatus, errorThrown) {
                        console.log(jqXHR.responseText);
                    });
        }

    });
    return Task;
});
