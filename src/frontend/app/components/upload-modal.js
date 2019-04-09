import Component from '@ember/component';
import { computed } from '@ember/object';
import { inject } from '@ember/service';

export default Component.extend({
  ajax: inject(),
  hasImages: false,
  imageCount: 0,
  fd: computed(() => {
    return new FormData();
  }),
  actions: {
    addImages: function(e) {
      let files = e.target.files;
      for (let i = 0; i < files.length; i++) {
        this.fd.append(`image[${this.imageCount}]`, files[i]);
        this.imageCount++;
      }
      this.set('hasImages', true);
    },
    uploadImages: function() {
      if (this.hasImages) {
        this.toggleLoading();
        $.ajax({
          url: 'http://localhost:5000/upload',
          method: 'POST',
          data: this.fd,
          processData: false,
          contentType: false,
          dataType: 'json',
          success: (response) => {
            this.toggleLoading();
            this.hideUpload();
            this.displayResult(response.val);
          },
          error: (e) => {
            console.log(e);
          }
        })
      }
    }
  }
});
