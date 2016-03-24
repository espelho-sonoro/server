import flask, os

app = flask.Flask(__name__, static_folder='public', static_url_path='')
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

@app.route('/')
def root():
    return app.send_static_file('index.html')
