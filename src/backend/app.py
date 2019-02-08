from flask import Flask, request
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
        print(request)
        print(request.files['image[0]'])
        print(len(request.files))
        for i in range(len(request.files)):
            file = request.files['image[{}]'.format(i)]
            filename = secure_filename(file.filename)
            #cv2.imwrite(filename, request.files['image[{}]'.format(i)])
            file.save('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))

        return json.dumps({'status': 'OK', 'val': 'Tested'})
    else:
        return json.dumps({'status': 'false', 'val': 'Not Tested'})


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host='0.0.0.0')
