import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click, fillIn } from '@ember/test-helpers';
import { keyEvent } from 'ember-native-dom-helpers';
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage';
import hbs from 'htmlbars-inline-precompile';
import Service from '@ember/service';

const cookieStub = Service.extend({
  currentUser: 'Conor,Hanlon,conorbh97@gmail.com,1234,http://mock.url,mocktoken',
  read(cookieName) {
    return this.get('currentUser');
  }
});

module('Integration | Component | share-document', function(hooks) {
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
    this.set('hideShareDocument', () => {
      this.set('showShareDocument', false);
      this.set('documentId', null);
      this.set('documentTitle', null);
    });

    await render(hbs`{{share-document}}`);

    assert.equal($('#share-docs h5').text().trim(),
      'Please enter the email address(es) of the people you would like to share this document with.');

    // Template block usage:
    await render(hbs`
      {{#share-document title='TestShare' toggleLoading=toggleLoading hideShareDocument=hideShareDocument}}
      {{/share-document}}
    `);

    assert.equal($('#share-docs h2').text().trim(), 'Document Title: TestShare');

    await click('.ember-power-select-trigger-multiple-input');
    await keyEvent('.ember-power-select-trigger-multiple-input', 'keydown', 13);
    await click('.sign-in-btn');

    await click('.ember-power-select-trigger-multiple-input');
    await fillIn('.ember-power-select-trigger-multiple-input', 'mock.email@gmail.com');
    await keyEvent('.ember-power-select-trigger-multiple-input', 'keydown', 13);
    await click('#pButton3');
    await click('.sign-in-btn');
  });
});
