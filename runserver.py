from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from core import Manager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app.manager = Manager()

from views import *


if __name__ == '__main__':
    app.run()

