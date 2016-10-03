
define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone){
    var Video = Backbone.Model.extend({
        idAttribute: "id",
        urlRoot: 'http://stackannotator.com/api',
        post: function() {
            var self = this;
            return $.post(this.urlRoot + '/videos', self.attributes).done(function(data){
                   console.log(data);
            });
        },
        incrementAttr: function(attrType) {
            var self = this;
            return $.post(this.urlRoot + '/video/' + this.id +'/' + attrType).done(function(data) {
                //self.set(attrType+'s', data[attrType+'s']);
                self.set(data);
            });
        }
    });
    return Video;
});