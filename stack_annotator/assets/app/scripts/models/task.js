define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Task = Backbone.Model.extend({
        idAttribute: "id",
        urlRoot: 'http://stackannotator.com/api',
        post: function() {
            var self = this;
            return $.post(this.urlRoot + '/tasks', self.attributes).done(function(data){
                   console.log(data);
            });
        }
    });
    return Task;
});