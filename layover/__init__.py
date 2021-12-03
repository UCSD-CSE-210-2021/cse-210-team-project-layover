from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('layover.settings')
app.config.from_envvar('MY_ENV', silent=True)

print("DB URI IS: ", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

from layover import routes