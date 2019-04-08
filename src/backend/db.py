from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True)
    forename = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)
    access_token = db.Column(db.String(256), nullable=False)

    def __init__(self, id, forename, surname, email, image_url, access_token):
        self.id = id
        self.forename = forename
        self.surname = surname
        self.email = email
        self.image_url = image_url
        self.access_token = access_token


class CreatedDocument(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True)
    uid = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, id, uid, title):
        self.id = id
        self.uid = uid
        self.title = title

    def as_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'title': self.title,
            'created_on': self.created_on.__str__()
        }