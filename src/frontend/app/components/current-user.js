import Component from '@ember/component';
import { inject } from '@ember/service';

export default Component.extend({
  user: inject('user-service')
});
