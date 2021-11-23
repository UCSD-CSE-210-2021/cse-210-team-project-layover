from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from models import LayoverMeeting_SQLAlchemy, LayoverUser_SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from layover import routes