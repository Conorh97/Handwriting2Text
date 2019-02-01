import Service from '@ember/service';

export default Service.extend({
  forename: null,
  surname: null,
  email: null,
  id: null,
  imageUrl: null,
  accessToken: null,

  setUser(userInfo, accessToken) {
    this.set('forename', userInfo.name.givenName);
    this.set('surname', userInfo.name.familyName);
    this.set('email', userInfo.emails[0].value);
    this.set('id', userInfo.id);
    this.set('imageUrl', userInfo.image.url);
    this.set('accessToken', accessToken);

    localStorage.setItem('forename', JSON.stringify(this.forename));
    localStorage.setItem('surname', JSON.stringify(this.surname));
    localStorage.setItem('email', JSON.stringify(this.email));
    localStorage.setItem('id', JSON.stringify(this.id));
    localStorage.setItem('imageUrl', JSON.stringify(this.imageUrl));
    localStorage.setItem('accessToken', JSON.stringify(this.accessToken));
  },

  refreshUser() {
    let forename = this.forename;
    if (!forename) {
      let storedForename = JSON.parse(localStorage.forename);
      if (storedForename) {
        let storedSurname = JSON.parse(localStorage.surname);
        let storedEmail = JSON.parse(localStorage.email);
        let storedId = JSON.parse(localStorage.id);
        let storedImageUrl = JSON.parse(localStorage.imageUrl);
        let storedAccessToken = JSON.parse(localStorage.accessToken);

        this.set('forename', storedForename);
        this.set('surname', storedSurname);
        this.set('email', storedEmail);
        this.set('id', storedId);
        this.set('imageUrl', storedImageUrl);
        this.set('accessToken', storedAccessToken);
      }
    }
  }
});
