import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click } from '@ember/test-helpers';
import { authenticateSession } from 'ember-simple-auth/test-support';
import hbs from 'htmlbars-inline-precompile';
import Service from '@ember/service';

const cookieStub = Service.extend({
  currentUser: 'Conor,Hanlon,conorbh97@gmail.com,1234,http://mock.url,mocktoken',
  clear () {
    return this.get('currentUser', null);
  }
});

module('Integration | Component | page-header', function(hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function() {
    this.owner.register('service:cookies', cookieStub);
  });

  test('it renders', async function(assert) {
    await render(hbs`{{page-header}}`);

    assert.equal(this.element.textContent.trim(), 'Login with Google');

    await authenticateSession();

    assert.equal(this.element.textContent.trim(), 'Logout');
  });
});
