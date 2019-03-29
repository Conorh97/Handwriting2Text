import Component from '@ember/component';

export default Component.extend({
  upload: true,
  currentSlide: 0,
  actions: {
    showUploadSlides: function() {
      this.set('currentSlide', 0);
      this.set('upload', true);
    },
    showShareSlides: function () {
      this.set('currentSlide', 0);
      this.set('upload', false);
    },
    nextSlide: function () {
      if (this.upload) {
        if (this.currentSlide < 2) {
          this.set("currentSlide", this.currentSlide + 1);
        }
      } else {
        if (this.currentSlide < 1) {
          this.set("currentSlide", this.currentSlide + 1);
        }
      }
    },
    previousSlide: function () {
      if (this.currentSlide > 0) {
        this.set("currentSlide", this.currentSlide - 1);
      }
    }
  }
});
