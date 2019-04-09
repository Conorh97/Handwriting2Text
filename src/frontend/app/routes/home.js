import Route from '@ember/routing/route';
import { inject } from '@ember/service';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Route.extend(AuthenticatedRouteMixin, {
  cookies: inject(),
  ajax: inject(),
  setupController(controller) {
    let cookieService = this.get('cookies');
    let cookieInfo = cookieService.read('currentUser').split(',');
    let userId = cookieInfo[3];
    this.get('ajax').request(`http://localhost:5000/documents/${userId}`, {
      method: 'GET',
      success: (userInfo) => {
        if (userInfo.val.length > 0) {
          console.log(userInfo.val);
          controller.set('documents', userInfo.val);
        }
      }
    });
  }
});
