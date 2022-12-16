import secrets
from flask import session
from werkzeug.security import check_password_hash
from main.query import Query
from app import db

query = Query(db)

def process_login(username, password):
    user = query.get_login_credentials(username)

    if not user:
        pass

    else:
        password_hash = user['password']
        if check_password_hash(password_hash, password):
            default_portfolio = query.get_default_portfolio(user['id'])
            session['username'] = user['username']
            session['user_id'] = user['id']
            session['portfolio'] = default_portfolio
            session['csrf_token'] = secrets.token_hex(16)

        else:
            pass