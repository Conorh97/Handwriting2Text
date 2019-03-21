import Component from '@ember/component';
import { isBlank } from '@ember/utils';

export default Component.extend({
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
    permissionSelected() {
      this.set('permission', true);
    }
  }
});
