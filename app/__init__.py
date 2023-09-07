from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app,origins=["https://www.nutrimart.co.id"])
app.config.from_pyfile('config.py')
api=Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

from app import routes,models
