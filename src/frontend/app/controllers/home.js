import Controller from '@ember/controller';

export default Controller.extend({
  showShare: false,
  showUpload: false,
  showResult: false,
  showInstructions: false,
  result: null,
  actions: {
    displayShare: function() {
      this.set('showShare', true);
    },
    hideShare: function() {
      this.set('showShare', false);
    },
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
      this.set('result', null);
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
