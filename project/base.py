from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///twitter.db"
app.secret_key = "this is a secret key"

db = SQLAlchemy(app)
