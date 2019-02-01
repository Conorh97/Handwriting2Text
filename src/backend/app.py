from flask import Flask, send_from_directory

app = Flask(__name__, static_url_path='')


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('', path)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.config.update({
        'DEBUG': True,
    })
    app.run(host="0.0.0.0")
