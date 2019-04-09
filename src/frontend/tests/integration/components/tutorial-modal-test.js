import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | tutorial-modal', function(hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function(assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`{{tutorial-modal}}`);

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'First, click the blue box indicated in the image above.');

    await click('.next-slide');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'You can upload more images to be converted by clicking the box again.');

    await click('.next-slide');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'The resulting text is displayed in the large box. This can be edited before saving the document.');

    await click('#labelB2');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'The application keeps track of each document you save to Google Drive, allowing you to share them\n' +
      '                with your friends via email.');

    await click('.next-slide');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'You can add multiple email addresses to the input field shown above.');

    await click('.prev-slide');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'The application keeps track of each document you save to Google Drive, allowing you to share them\n' +
      '                with your friends via email.');

    await click('#labelB1');

    assert.equal($('.instructions ul li:first-child').text().trim(),
      'First, click the blue box indicated in the image above.');

    await click('.close-button');
  });
});
