import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | upload-modal', function(hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function(assert) {
    this.set('loading', false);
    this.set('toggleLoading', () => {
      let currentVal = this.get('loading');
      this.set('loading', !currentVal);
    });
    this.set('hideUpload', () => {
      this.set('showUpload', false);
    });
    this.set('displayResult', (r) => {
      this.set('result', r);
      this.set('showResult', true);
    });

    await render(hbs`
      {{#upload-modal toggleLoading=toggleLoading hideUpload=hideUpload displayResult=displayResult}}
      {{/upload-modal}}
    `);

    assert.equal($('h4').text().trim(), 'Upload');

    let inputElement = $('.imageInput');

    let blob = new Blob(['foo', 'bar'], {type: 'image/png'});
    blob.name = 'foobar.png';
    inputElement.triggerHandler({
      type: 'change',
      target: {
        files: {
          0: blob,
          length: 1,
          item() {
            return blob;
          }
        }
      }
    });

    await click('.imageInput');

    assert.equal($('h4').text().trim(), '1 image(s) added.');

    await click('#upload-box button');
  });
});
