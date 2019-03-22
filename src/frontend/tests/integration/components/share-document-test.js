import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | share-document', function(hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function(assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`{{share-document}}`);

    assert.equal($('#share-docs h5').text().trim(),
      'Please enter the email address(es) of the people you would like to share this document with.');

    // Template block usage:
    await render(hbs`
      {{#share-document title='TestShare'}}
      {{/share-document}}
    `);

    assert.equal($('#share-docs h2').text().trim(), 'Document Title: TestShare');
  });
});
