import Mirage from 'ember-cli-mirage';

export default function() {
  /*
  this.get('router.url', () => {
    return 'http://localhost:4200/callback' +
      '#access_token=mock_token' +
      '&token_type=Bearer&' +
      'expires_in=3600' +
      '&scope=mock_scope' +
      '&authuser=0' +
      '&session_state=7b77c9c290a9943ccee0d5bc4e940039e1295762..e55f' +
      '&prompt=consent'
  })
  */
  this.urlPrefix = 'http://localhost:5000';

  this.get('/documents/:user_id', {
    val: [
        {'id': 'mock_id1', 'uid': 'mock_uid1', 'title': 'TestDB8', 'created_on': '2019-03-21 19:05:41'},
        {'id': 'mock_id2', 'uid': 'mock_uid2', 'title': 'TestDB7', 'created_on': '2019-03-21 13:13:25'}
    ]}
  );

  this.post('/create_user', {status: 'User Created'});

  this.get(`https://www.googleapis.com/plus/v1/people/me`, () => {
    console.log('Hit');
    return {
      name: {
        givenName: 'Joe',
        familyName: 'Bloggs'
      },
      emails: [
        {value: 'joebloggs@gmail.com'}
      ],
      id: 'mock_id',
      image: {
        url: 'mock_url'
      }
    }
  });
}
