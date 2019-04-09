import Route from '@ember/routing/route';
import { later } from '@ember/runloop';
import { inject } from '@ember/service';
import OAuth2ImplicitGrantCallbackRouteMixin from 'ember-simple-auth/mixins/oauth2-implicit-grant-callback-route-mixin';

export default Route.extend(OAuth2ImplicitGrantCallbackRouteMixin, {
  ajax: inject(),
  cookies: inject(),
  authenticator: 'authenticator:oauth2-implicit-grant',
  beforeModel: function () {
    let responseUrl = window.location.href;
    let access_token = responseUrl.split('&')[0].split('=')[1];
    let queryUrl = `https://www.googleapis.com/plus/v1/people/me?access_token=${access_token}`;
    this.get('ajax').request(queryUrl, {
      method: 'GET',
      success: (userInfo) => {
        this.createCookie(userInfo, access_token);
        console.log(userInfo);
        later(() => {
          console.log('Go Home');
          this.transitionTo('home');
        }, 1000);
      }
    });
  },
  createCookie: function(user, accessToken) {
    let forename = user.name.givenName;
    let surname = user.name.familyName;
    let email = user.emails[0].value;
    let id = user.id;
    let imageUrl = user.image.url;
    let token = accessToken;

    let cookieContent = forename + "," + surname + "," + email
                        + "," + id  + "," + imageUrl  + "," + token;

    let cookieService = this.get('cookies');
    cookieService.write('currentUser', cookieContent);

    this.get('ajax').request('http://localhost:5000/create_user', {
      method: 'POST',
      data: {
        id: id,
        forename: forename,
        surname: surname,
        email: email,
        imageUrl: imageUrl,
        accessToken: accessToken
      },
      dataType: 'json',
      success: (result) => {
        console.log(result);
      }
    })
  }
});
