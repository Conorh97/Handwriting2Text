import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | share-modal', function(hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function(assert) {
    this.set('displayShareDocument', (documentId, documentTitle) => {
      this.set('showShare', false);
      this.set('showShareDocument', true);
      this.set('documentId', documentId);
      this.set('documentTitle', documentTitle);
    });

    await render(hbs`{{share-modal}}`);

    assert.equal($('#no-docs h2').text().trim(), 'Oops!');
    /*
    this.set('documents', [
      {'id': 'mock_id1', 'uid': 'mock_uid1', 'title': 'TestDB8', 'created_on': '2019-03-21 19:05:41'},
      {'id': 'mock_id2', 'uid': 'mock_uid2', 'title': 'TestDB7', 'created_on': '2019-03-21 13:13:25'}
    ]);

    await render(hbs`
      {{#share-document documents=documents displayShareDocument=displayShareDocument}}
      {{/share-document}}
    `);

    assert.equal($('.document-card-even h4').text().trim(), 'TestDB7');

    await click('.document-card-odd .share-btn');

    assert.equal(this.get('documentId'), 'mock_uid1');
    */
  });
});
