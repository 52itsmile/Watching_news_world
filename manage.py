from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

class Config(object):
    DEBUG = True
app.config.from_object(Config)

if __name__ == "__main__":
    app.run()