from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from image import process_image
from docx import Document
from io import BytesIO
import os
import json

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
