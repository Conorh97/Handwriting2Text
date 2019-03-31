from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from image import process_image
from docx import Document
from io import BytesIO
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from model.Model import Model
from model.Loader import Loader
from spellchecker import SpellChecker
import os
import json

character_list_path = 'model/character_list.txt'
data_path = './tmp-images/'
image_width = 128
image_height = 32
batch_size = 1
max_text_length = 32

SCOPES = ['https://www.googleapis.com/auth/documents']
DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:p4ssw0rd@localhost/H2TXT'
db = SQLAlchemy(app)

with open(character_list_path, "r+") as f:
    character_list = sorted(list(f.read()))
model = Model(image_width, image_height, batch_size, character_list, max_text_length, False, True)


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


def callback(request_id, response, exception):
    if exception:
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


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
            os.remove('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))

        data_loader = Loader(data_path, batch_size, (image_width, image_height), max_text_length, True)
        spell = SpellChecker()

        while data_loader.has_next():
            batch = data_loader.get_next()
            predicted = model.infer_single_batch(batch)

            for i in range(len(predicted)):
                print(predicted[i])
                corrected = spell.correction(predicted[i])
                print(corrected)
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


@app.route('/documents/<string:user_id>', methods=['GET'])
@cross_origin()
def documents(user_id):
    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            with open('credentials.json') as f:
                creds = json.load(f)

            client_id = creds['web']['client_id']
            client_secret = creds['web']['client_secret']
            token_uri = creds['web']['token_uri']

            user_creds = Credentials(token=user.access_token, token_uri=token_uri,
                                     client_id=client_id, client_secret=client_secret)
            service = build('drive', 'v3', credentials=user_creds)

            drive_files = service.files().list().execute()
            drive_ids = [file['id'] for file in drive_files['files']]
            user_documents = CreatedDocument.query.filter_by(uid=user_id).all()

            json_docs = []
            for doc in user_documents:
                if doc.id in drive_ids:
                    json_docs.append(doc.as_dict())
                else:
                    CreatedDocument.query.filter_by(id=doc.id).delete()

            db.session.commit()
            return json.dumps({'status': '201', 'val': json_docs})
        else:
            return json.dumps({'status': '500', 'val': 'Error'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app.route('/share_document', methods=['POST'])
@cross_origin()
def share_document():
    if request.form is not None:
        id = str(request.form['id'])
        uid = str(request.form['uid'])
        emails = [request.form['emails[{}]'.format(i)] for i in range(len(request.form) - 3)]
        permission = str(request.form['permission'])

        user = User.query.filter_by(id=uid).first()
        if user is not None:
            with open('credentials.json') as f:
                creds = json.load(f)

            client_id = creds['web']['client_id']
            client_secret = creds['web']['client_secret']
            token_uri = creds['web']['token_uri']

            user_creds = Credentials(token=user.access_token, token_uri=token_uri,
                                     client_id=client_id, client_secret=client_secret)
            service = build('drive', 'v3', credentials=user_creds)
            batch = service.new_batch_http_request(callback=callback)

            for email in emails:
                user_permission = {
                    'type': 'user',
                    'role': permission,
                    'emailAddress': email
                }
                batch.add(service.permissions().create(
                    fileId=id,
                    body=user_permission,
                    fields='id'
                ))

            batch.execute()
            return json.dumps({'status': '201', 'val': 'Document shared successfully.'})
        else:
            return json.dumps({'status': '500', 'val': 'Error fetching access token.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')

