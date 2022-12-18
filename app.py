from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL').replace('://', 'ql://', 1)
app.secret_key = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

from main import routes
