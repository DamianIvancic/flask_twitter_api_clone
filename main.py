from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import api as api_blueprint
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['IMAGE_FORMAT'] = '.png'
db = SQLAlchemy(app)


app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    app.run()


