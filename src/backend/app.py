from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from image import process_image
import os
import json

DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())
app = Flask(__name__, static_url_path='')


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    if request.form is not None:
        for i in range(len(request.files)):
            file = request.files['image[{}]'.format(i)]
            filename = secure_filename(file.filename)
            file.save('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))
            process_image(filename)
        return json.dumps({'status': '201', 'val': 'This is some template result text to fill the textarea.'})
    else:
        return json.dumps({'status': '500', 'val': 'Error'})


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')
