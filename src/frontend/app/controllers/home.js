import Controller from '@ember/controller';

export default Controller.extend({
  loading: false,
  showShare: false,
  showUpload: false,
  showResult: false,
  showInstructions: false,
  showShareDocument: false,
  result: null,
  documentId: null,
  documentTitle: null,
  actions: {
    toggleLoading: function() {
      console.log(this.loading);
      this.toggleProperty('loading');
    },
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
    },
    displayShareDocument: function(documentId, documentTitle) {
      this.set('showShare', false);
      this.set('showShareDocument', true);
      this.set('documentId', documentId);
      this.set('documentTitle', documentTitle);
    },
    hideShareDocument: function() {
      this.set('showShareDocument', false);
      this.set('documentId', null);
      this.set('documentTitle', null);
    }
  }
});
