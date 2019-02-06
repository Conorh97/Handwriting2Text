import Component from '@ember/component';
import { inject as service } from '@ember/service';
import config from '../config/environment';

export default Component.extend({
  router: service(),
  session: service(),
  cookies: service(),
  actions: {
    invalidateSession() {
      let cookieService = this.get('cookies');
      cookieService.clear('user');

      this.get('session').invalidate();
      this.get('router').transitionTo('login');
    },
    authenticate() {
      let clientId = config.googleClientID;
      let redirectURI = `http://localhost:4200/callback`;
      let responseType = `token`;
      let scope = `email`;
      window.location.replace(`https://accounts.google.com/o/oauth2/v2/auth?`
        + `client_id=${clientId}`
        + `&redirect_uri=${redirectURI}`
        + `&response_type=${responseType}`
        + `&scope=${scope}`
      );
    }
  }
});