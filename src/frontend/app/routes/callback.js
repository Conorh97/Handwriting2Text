import Route from '@ember/routing/route';
import { later } from '@ember/runloop';
import { inject } from '@ember/service';
import OAuth2ImplicitGrantCallbackRouteMixin from 'ember-simple-auth/mixins/oauth2-implicit-grant-callback-route-mixin';

export default Route.extend(OAuth2ImplicitGrantCallbackRouteMixin, {
  ajax: inject(),
  user: inject('user-service'),
  authenticator: 'authenticator:oauth2-implicit-grant',
  afterModel: function () {
    let responseUrl = this.get('router.url');
    let access_token = responseUrl.split('&')[0].split('=')[1];
    let queryUrl = `https://www.googleapis.com/plus/v1/people/me?access_token=${access_token}`;
    this.get('ajax').request(queryUrl, {
      method: 'GET',
      async: false,
      success: (userInfo) => {
        this.user.setUser(userInfo, access_token);
        later(() => {
          this.transitionTo('protected');
        }, 1000);
      },
      error: (e) => {
        console.log(e);
      }
    });
  }
});
