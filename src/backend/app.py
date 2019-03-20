from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from image import process_image
from docx import Document
from io import BytesIO
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import json


SCOPES = ['https://www.googleapis.com/auth/documents']
DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:p4ssw0rd@localhost/H2TXT'
db = SQLAlchemy(app)


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


db.create_all()
db.session.commit()


@app.route('/create_user', methods=['POST'])
@cross_origin()
def create_user():
    if request.form is not None:
        id = str(request.form['id'])
        user = User.query.filter_by(id=id).first()
        if user is not None:
            access_token = str(request.form['accessToken'])
            if access_token != user.access_token:
                user.access_token = access_token
                db.session.commit()
                return json.dumps({'status': '201', 'val': 'Access token updated.'})
            else:
                return json.dumps({'status': '201', 'val': 'Access token up to date.'})
        else:
            forename = str(request.form['forename'])
            surname = str(request.form['surname'])
            email = str(request.form['email'])
            image_url = str(request.form['imageUrl'])
            access_token = str(request.form['accessToken'])
            user = User(id, forename, surname, email, image_url, access_token)
            db.session.add(user)
            db.session.commit()
            return json.dumps({'status': '201', 'val': 'New user created.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    if request.files is not None:
        for i in range(len(request.files)):
            file = request.files['image[{}]'.format(i)]
            filename = secure_filename(file.filename)
            file.save('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))
            process_image(filename)
        return json.dumps({'status': '201', 'val': 'This is some template result text to fill the textarea.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app.route('/create', methods=['POST'])
@cross_origin()
def create():
    if request.form is not None:
        filename = str(request.form['filename'])
        content = str(request.form['content'])
        access_token = str(request.form['accessToken'])

        user = User.query.filter_by(access_token=access_token).first()

        if user is not None:
            with open('credentials.json') as f:
                creds = json.load(f)

            client_id = creds['web']['client_id']
            client_secret = creds['web']['client_secret']
            token_uri = creds['web']['token_uri']

            user_creds = Credentials(token=access_token, token_uri=token_uri,
                                     client_id=client_id, client_secret=client_secret)
            service = build('docs', 'v1', credentials=user_creds)

            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': content
                    }
                }
            ]

            doc = service.documents().create(body={'title': filename}).execute()
            document_id = doc['documentId']
            insert_text = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

            document = CreatedDocument(document_id, user.id, filename)
            db.session.add(document)
            db.session.commit()
            return json.dumps({'status': '201', 'val': 'Google Doc Created'})
        else:
            return json.dumps({'status': '500', 'val': 'Access token expired.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})

# Not downloading on client side, will revisit


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
    if request.form is not None:
        filename = str(request.form['filename'])
        content = str(request.form['content'])
        doc = Document()
        doc.add_heading(filename, 0)
        doc.add_paragraph(content)
        newFile = BytesIO()
        doc.save(newFile)
        newFile.seek(0)
        return send_file(newFile, as_attachment=True, attachment_filename='{}.doc'.format(filename))
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app.route('/documents/<string:user_id>', methods=['GET'])
@cross_origin()
def documents(user_id):
    if user_id is not None:
        documents = CreatedDocument.query.filter_by(uid=user_id).all()
        json_docs = [doc.as_dict() for doc in documents]
        return json.dumps({'status': '201', 'val': json_docs})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')
