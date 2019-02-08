import Controller from '@ember/controller';

export default Controller.extend({
  showUpload: false,
  showInstructions: false,
  actions: {
    displayUpload: function() {
      this.set('showUpload', true);
    },
    hideUpload: function() {
      this.set('showUpload', false);
    },
    displayInstructions: function() {
      this.set('showInstructions', true);
    },
    hideInstructions: function() {
      this.set('showInstructions', false);
    }
  }
});
