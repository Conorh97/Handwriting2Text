import Component from '@ember/component';
import { inject } from '@ember/service';
import { computed } from '@ember/object';
import FileSaverMixin from 'ember-cli-file-saver/mixins/file-saver';

export default Component.extend(FileSaverMixin, {
  ajax: inject(),
  cookies: inject(),
  noName: false,
  fd: computed(() => {
    return new FormData();
  }),
  actions: {
    downloadFile: function() {
      let filename = this.get('filename');
      let content = this.result;
      if (filename != null) {
        this.set('noName', false);
        this.saveFileAs(filename + '.doc', content, 'application/msword');
      } else {
        this.set('noName', true);
      }
    },
    createGoogleDoc: function() {
      let filename = this.get('filename');
      let content = this.result;
      if (filename != null) {
        this.set('noName', false);
        this.fd.append('filename', filename);
        this.fd.append('content', content);
        let accessToken = this.getToken();
        if (accessToken) {
          this.toggleLoading();
          this.fd.append('accessToken', accessToken);
          $.ajax({
            url: 'http://localhost:5000/create',
            method: 'POST',
            data: this.fd,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: (response) => {
              this.toggleLoading();
            },
            error: (e) => {
              console.log(e);
            }
          })
        }
      } else {
        this.set('noName', true);
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
