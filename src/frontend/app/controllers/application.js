import Controller from '@ember/controller';
import { inject as service } from '@ember/service';

export default Controller.extend({
  session: service(),
  cookies: service(),
  user: null,
  init: function(controller, model) {
    this._super(controller, model);

    let cookieService = this.get('cookies');
    let cookie = cookieService.read('currentUser');

    if (cookie) {
      let values = cookie.split(',');
      let currentUser = {
        forename: values[0],
        surname: values[1],
        email: values[2],
        id: values[3],
        imageUrl: values[4],
        accessToken: values[5]
      };

      this.user = currentUser;
    }
  }
});
