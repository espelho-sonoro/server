import flask

app = flask.Flask(__name__, static_folder='public', static_url_path='')
app.run()

@app.route('/')
def root():
    return app.send_static_file('index.html')
