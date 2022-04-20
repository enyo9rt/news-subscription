from flask import Flask

app = Flask(__name__)


@app.route('/')
def harmony():
    return "<h1>Harmony</h1>"


if __name__ == "__main__":
    app.run()
