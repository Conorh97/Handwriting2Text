import Component from '@ember/component';
import { inject } from '@ember/service';
import { computed } from '@ember/object';

export default Component.extend({
  ajax: inject(),
  fd: computed(() => {
    return new FormData();
  }),
  actions: {
    downloadFile: function() {
      let filename = this.get('filename');
      let content = this.result;
      if (filename != null) {
        this.fd.append('filename', filename);
        this.fd.append('content', content);
        $.ajax({
          url: 'http://localhost:5000/download',
          method: 'POST',
          data: this.fd,
          processData: false,
          contentType: false,
          dataType: 'json',
          success: (response) => {
            this.hideResult();
            console.log(response);
            console.log(response.data);
          },
          error: (e) => {
            console.log(e);
          }
        })
      }
    }
  }
});
