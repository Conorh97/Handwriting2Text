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
  },
  write(cookieName, content) {
    this.set('currentUser', content);
  }
});

module('Acceptance | callback', function(hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function() {
    this.owner.register('service:cookies', cookieStub);
  });

  test('visiting /callback', async function(assert) {
    await authenticateSession();
    await visit('/callback#token=mock_token&type=mock_type');

    assert.notEqual(currentURL(), '/callback#token=mock_token&type=mock_type');
  });
});
