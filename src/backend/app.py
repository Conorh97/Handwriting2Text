from flask import Flask, request, send_file
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

        with open('credentials.json') as f:
            creds = json.load(f)

        client_id = creds['installed']['client_id']
        client_secret = creds['installed']['client_secret']
        token_uri = creds['installed']['token_uri']

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

        return json.dumps({'status': '201', 'val': 'Google Doc Created'})
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


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')
