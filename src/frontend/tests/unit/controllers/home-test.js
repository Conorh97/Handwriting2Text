import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Controller | home', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('toggle loading', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('toggleLoading');
    assert.equal(controller.get('loading'), true);

    controller.send('toggleLoading');
    assert.equal(controller.get('loading'), false);
  });

  test('show share modal', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('displayShare');
    assert.equal(controller.get('showShare'), true);

    controller.send('hideShare');
    assert.equal(controller.get('showShare'), false);
  });

  test('show upload modal', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('displayUpload');
    assert.equal(controller.get('showUpload'), true);

    controller.send('hideUpload');
    assert.equal(controller.get('showUpload'), false);
  });

  test('show tutorial modal', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('displayTutorial');
    assert.equal(controller.get('showTutorial'), true);

    controller.send('hideTutorial');
    assert.equal(controller.get('showTutorial'), false);
  });

  test('show results modal', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('displayResult', 'Test result.');
    assert.equal(controller.get('showResult'), true);
    assert.equal(controller.get('result'), 'Test result.');

    controller.send('hideResult');
    assert.equal(controller.get('showResult'), false);
    assert.equal(controller.get('result'), null);
  });

  test('show share document modal', function(assert) {
    let controller = this.owner.lookup('controller:home');
    assert.ok(controller);

    controller.send('displayShare');
    controller.send('displayShareDocument', '12345678', 'Test Document');
    assert.equal(controller.get('showShare'), false);
    assert.equal(controller.get('showShareDocument'), true);
    assert.equal(controller.get('documentId'), '12345678');
    assert.equal(controller.get('documentTitle'), 'Test Document');

    controller.send('hideShareDocument');
    assert.equal(controller.get('showShareDocument'), false);
    assert.equal(controller.get('documentId'), null);
    assert.equal(controller.get('documentTitle'), null);
  });
});
