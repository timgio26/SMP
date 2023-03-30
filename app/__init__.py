from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('config.py')
api=Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

from app import routes,models
