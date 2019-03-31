import Controller from '@ember/controller';

export default Controller.extend({
  loading: false,
  showShare: false,
  showUpload: false,
  showResult: false,
  showShareDocument: false,
  showTutorial: false,
  result: null,
  documentId: null,
  documentTitle: null,
  actions: {
    toggleLoading: function() {
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
    },
    displayTutorial: function() {
      this.set('showTutorial', true);
    },
    hideTutorial: function() {
      this.set('showTutorial', false);
    }
  }
});
