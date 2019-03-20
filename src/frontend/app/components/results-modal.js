import Component from '@ember/component';
import { inject } from '@ember/service';
import { computed } from '@ember/object';

export default Component.extend({
  ajax: inject(),
  cookies: inject(),
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
          },
          error: (e) => {
            console.log(e);
          }
        })
      }
    },
    createGoogleDoc: function() {
      let filename = this.get('filename');
      let content = this.result;
      if (filename != null) {
        this.fd.append('filename', filename);
        this.fd.append('content', content);
        let accessToken = this.getToken();
        if (accessToken) {
          this.fd.append('accessToken', accessToken);
          $.ajax({
            url: 'http://localhost:5000/create',
            method: 'POST',
            data: this.fd,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: (response) => {
              this.hideResult();
            },
            error: (e) => {
              console.log(e);
            }
          })
        }
      }
    }
  },
  getToken: function() {
    let cookieService = this.get('cookies');
    let cookie = cookieService.read('currentUser');
    if (cookie) {
      let accessToken = cookie.split(',')[5];
      return accessToken;
    } else {
      return null;
    }
  }
});
