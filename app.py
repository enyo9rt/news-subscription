from flask import Flask

app = Flask(__name__)


@app.route('/')
def harmony():
    return "<h2>Harmony</h2>"


if __name__ == "__main__":
    app.run()
