import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click, fillIn } from '@ember/test-helpers';
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage';
import hbs from 'htmlbars-inline-precompile';
import Service from '@ember/service';

const cookieStub = Service.extend({
  currentUser: 'Conor,Hanlon,conorbh97@gmail.com,1234,http://mock.url,mocktoken',
  read(cookieName) {
    return this.get('currentUser');
  }
});

module('Integration | Component | results-modal', function(hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function() {
    this.owner.register('service:cookies', cookieStub);
  });

  test('it renders', async function(assert) {
    this.set('loading', false);
    this.set('toggleLoading', () => {
      let currentVal = this.get('loading');
      this.set('loading', !currentVal);
    });

    await render(hbs`{{results-modal}}`);

    assert.equal($('.results-area label').text().trim(), 'Converted Text:');

    await click('.save-doc-btn');
    await click('.download-btn');

    assert.equal($('.error-message').text().trim(), 'Please enter a filename above.');

    await render(hbs`
      {{#results-modal result="Sample result text." toggleLoading=toggleLoading}}
      {{/results-modal}}
    `);

    await fillIn('.new-file-name', 'Testing File');
    await click('.save-doc-btn');
    await click('.download-btn');
  });
});
