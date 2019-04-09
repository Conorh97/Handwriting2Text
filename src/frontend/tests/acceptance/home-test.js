import { module, test } from 'qunit';
import { visit, currentURL } from '@ember/test-helpers';
import { setupApplicationTest } from 'ember-qunit';
import { authenticateSession } from 'ember-simple-auth/test-support';
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage';
import Service from '@ember/service';

const cookieStub = Service.extend({
  currentUser: 'Conor,Hanlon,conorbh97@gmail.com,1234,http://mock.url,mocktoken',
  read(cookieName) {
    return this.get('currentUser');
  }
});

module('Acceptance | home', function(hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function() {
    this.owner.register('service:cookies', cookieStub);
  });

  test('visiting /home', async function(assert) {
    await authenticateSession();
    await visit('/home');

    assert.equal(currentURL(), '/home');
  });
});
