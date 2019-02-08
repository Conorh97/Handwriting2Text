from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
import json
import cv2
import os

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
        return Response({'val': 'Image(s) Uploaded'}, status=201, mimetype='application/json')
    else:
        return Response({'val': 'Error in uploading'}, status=500, mimetype='application/json')


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')
