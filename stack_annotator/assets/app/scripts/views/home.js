define([
  'jquery',
  'underscore',
  'backbone',
  // Templates
  'text!../templates/home.html'
], function($, _, Backbone, homeTemplate){
  var HomeView = Backbone.View.extend({
      el: $('.container'),
      render: function() {
          var data = {};
          var compiledTemplate = _.template(homeTemplate, data);
          this.$el.empty().append(compiledTemplate);
      }
  });
  return HomeView;
});
