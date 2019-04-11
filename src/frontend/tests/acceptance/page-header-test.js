import { module, test } from 'qunit';
import { visit, currentURL, click } from '@ember/test-helpers';
import { setupApplicationTest } from 'ember-qunit';
import { authenticateSession } from 'ember-simple-auth/test-support';
import Service from '@ember/service';

const cookieStub = Service.extend({
  currentUser: 'Conor,Hanlon,conorbh97@gmail.com,1234,http://mock.url,mocktoken',
  clear () {
    return this.get('currentUser', null);
  },
  read(cookieName) {
    return this.get('currentUser');
  }
});

module('Acceptance | page header', function(hooks) {
  setupApplicationTest(hooks);

  hooks.beforeEach(function() {
    this.owner.register('service:cookies', cookieStub);
  });
  /*
  test('validating page-header functions', async function(assert) {
    await authenticateSession();

    await visit('/home');
    await click('.sign-out-btn');

    assert.equal(currentURL(), '/login');
  });
  */
});
