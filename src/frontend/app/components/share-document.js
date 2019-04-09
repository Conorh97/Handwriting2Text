import Component from '@ember/component';
import { isBlank } from '@ember/utils';
import { inject } from '@ember/service';

export default Component.extend({
  ajax: inject(),
  cookies: inject(),
  selected: [],
  permission: null,
  actions: {
    createOnEnter: function(select, e) {
      if (e.keyCode === 13 && select.isOpen &&
        !select.highlighted && !isBlank(select.searchText)) {

        let selected = this.get('selected');
        if (!selected.includes(select.searchText)) {
          select.actions.choose(select.searchText);
        }
      }
    },
    shareDocument: function() {
      if (this.selected.length > 0 && this.permission != null) {
        let cookieService = this.get('cookies');
        let cookieInfo = cookieService.read('currentUser').split(',');
        let userId = cookieInfo[3];
        let emails = {};
        for (let i = 0; i < this.selected.length; i++) {
          emails[i] = this.selected[i];
        }
        this.toggleLoading();
        this.get('ajax').request('http://localhost:5000/share_document', {
          method: 'POST',
          data: {
            id: this.id,
            uid: userId,
            emails: emails,
            permission: this.permission
          },
          dataType: 'json',
          success: (result) => {
            this.toggleLoading();
            this.hideShareDocument();
            console.log(result);
          }
        });
      }
    }
  }
});
