import Controller from '@ember/controller';
import { inject as service } from '@ember/service';
import config from '../config/environment';

export default Controller.extend({
  session: service('session'),
  actions: {
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
