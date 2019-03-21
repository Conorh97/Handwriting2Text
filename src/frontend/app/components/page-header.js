import Component from '@ember/component';
import { inject as service } from '@ember/service';
import config from '../config/environment';

export default Component.extend({
  ajax: service(),
  router: service(),
  session: service(),
  cookies: service(),
  actions: {
    invalidateSession: function() {
      let cookieService = this.get('cookies');
      cookieService.clear('user');

      this.get('session').invalidate();
      this.get('router').transitionTo('login');
    },
    authenticate: function() {
      let clientId = config.googleClientID;
      let redirectURI = `http://localhost:4200/callback`;
      let responseType = `token`;
      let scope = `email https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive`;
      let queryUrl = `https://accounts.google.com/o/oauth2/v2/auth?`
        + `client_id=${clientId}`
        + `&redirect_uri=${redirectURI}`
        + `&response_type=${responseType}`
        + `&scope=${scope}`;
      window.location.replace(queryUrl);
    }
  }
});
