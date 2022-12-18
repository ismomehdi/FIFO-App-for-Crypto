from flask import render_template, request, redirect, session
from services.create_tx_dict import create_tx_dict
from services.process_login import process_login
from services.process_signup import process_signup, username_exists
from services.check_csrf import check_csrf
from services.errors import feedback_errors
from app import app, db
from main.query import Query

query = Query(db)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    process_login(username, password)

    return redirect('/')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/submit/signup', methods=['POST'])
def submit_signup():
    username = request.form['username']
    password = request.form["password"]

    if username_exists(username):
        return render_template("error.html", 
            message="Oops, username already exists. Please choose another one.",
            link="/signup")

    process_signup(username, password)
    return redirect("/")


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/buy')
def buy():
    return render_template('buy.html')


@app.route('/sell')
def sell():
    return render_template('sell.html')


@app.route('/submit/buy', methods=['POST'])
def submit_buy():
    check_csrf()
    tx_data = create_tx_dict('buy')
    query.submit_tx(tx_data)

    return redirect('/buy')


@app.route('/submit/sell', methods=['POST'])
def submit_sell():
    check_csrf()
    tx_data = create_tx_dict('sell')
    query.submit_tx(tx_data)

    return redirect('/sell')


@app.route('/submit/feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']

    feedback_errors(name, message)
    query.submit_feedback(name, message)

    return redirect('/')


@app.route('/transactions')
def transactions():
    portfolio_id = session['portfolio']
    transactions = query.get_transaction_history(portfolio_id)

    return render_template('transactions.html', transactions=transactions)
