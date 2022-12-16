from flask import request
from main.query import Query
from app import db
from werkzeug.security import generate_password_hash

query = Query(db)

def process_signup(username, password):
    if query.username_exists(username):
        return 'Username already exists'

    pwd_hash = generate_password_hash(password)
    query.signup(username, pwd_hash)