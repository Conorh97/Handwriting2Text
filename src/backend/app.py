from flask import Flask, request, Blueprint
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from image import process_image
from model.Model import Model
from model.Loader import Loader
from spellchecker import SpellChecker
from db import db, User, CreatedDocument
from google_requests import create_doc, get_docs, share_doc
import os
import json
import string

character_list_path = 'model/character_list.txt'
data_path = './tmp-images/'
image_width = 128
image_height = 32
batch_size = 1
max_text_length = 32

with open(character_list_path, "r+") as f:
    character_list = sorted(list(f.read()))
model = Model(image_width, image_height, batch_size, character_list, max_text_length, False, True)

DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:p4ssw0rd@localhost/H2TXT'
app_blueprint = Blueprint('app_blueprint', __name__)

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()


@app_blueprint.route('/create_user', methods=['POST'])
@app.route('/create_user', methods=['POST'])
@cross_origin()
def create_user():
    if request.form is not None or len(request.form) == 0:
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


@app_blueprint.route('/upload', methods=['POST'])
@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    if request.files is not None:
        result = ""

        print(len(request.files))
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
                    if predicted[i][-1] in string.punctuation and len(predicted[i]) > 1:
                        corrected += predicted[i][-1]
                    if predicted[i][0].isupper():
                        corrected = corrected.replace(corrected[0], corrected[0].upper())
                    result += corrected
                    result += " "

            for filename in os.listdir(DOWNLOAD_DIRECTORY):
                os.remove('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))

        return json.dumps({'status': '201', 'val': result})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app_blueprint.route('/create', methods=['POST'])
@app.route('/create', methods=['POST'])
@cross_origin()
def create():
    if request.form is not None:
        filename = str(request.form['filename'])
        content = str(request.form['content'])
        access_token = str(request.form['accessToken'])

        user = User.query.filter_by(access_token=access_token).first()
        if user is not None:
            document_id = create_doc(access_token, content, filename)

            document = CreatedDocument(document_id, user.id, filename)
            db.session.add(document)
            db.session.commit()
            return json.dumps({'status': '201', 'val': 'Google Doc Created'})
        else:
            return json.dumps({'status': '500', 'val': 'Access token expired.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


@app_blueprint.route('/documents/<string:user_id>', methods=['GET'])
@app.route('/documents/<string:user_id>', methods=['GET'])
@cross_origin()
def documents(user_id):
    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            drive_files = get_docs(user.access_token)
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


@app_blueprint.route('/share_document', methods=['POST'])
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
            share_doc(user.access_token, emails, permission, id)
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

