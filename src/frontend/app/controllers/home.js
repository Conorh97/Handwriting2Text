import Controller from '@ember/controller';

export default Controller.extend({
  showUpload: false,
  showResult: false,
  showInstructions: false,
  result: null,
  actions: {
    displayUpload: function() {
      this.set('showUpload', true);
    },
    hideUpload: function() {
      this.set('showUpload', false);
    },
    displayResult: function(r) {
      this.set('result', r);
      this.set('showResult', true);
    },
    hideResult: function() {
      this.set('showResult', false);
    },
    displayInstructions: function() {
      this.set('showInstructions', true);
    },
    hideInstructions: function() {
      this.set('showInstructions', false);
    }
  }
});
