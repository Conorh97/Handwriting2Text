import Component from '@ember/component';

export default Component.extend({
  actions: {
    selectDocument: function(id, title) {
      this.displayShareDocument(id, title);
    }
  }
});
