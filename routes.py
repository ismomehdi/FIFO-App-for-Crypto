from flask import render_template, request, redirect, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from db.sql_queries import SQLQuery
import secrets

sql =  SQLQuery(db)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = sql.login(username)

    if not user:
        pass
    else:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
        else:
            pass

    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/signup")
def signup():
    return render_template("signup.html")


# FIX ERROR HANDLING
@app.route("/submit/signup", methods=["POST"])
def submit_signup():
    username = request.form["username"]
    pwd_hash = generate_password_hash(request.form["password"])

    sql.signup(username, pwd_hash) 

    return redirect("/")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/buy")
def buy():
    return render_template("buy.html")


@app.route("/sell")
def sell():
    return render_template("sell.html")

# FIX ERROR HANDLING
@app.route("/submit/buy", methods=["POST"])
def submit_buy():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    tx_details = {}

    tx_details["datetime"] = request.form["datetime"]
    tx_details["ticker"] = request.form["ticker"]
    tx_details["amount"] = request.form["amount"]
    tx_details["price"] = request.form["price"]
    tx_details["note"] = request.form["note"]
    tx_details["user_id"] = session["user_id"]

    sql.submit_tx(tx_details, "buy")

    return redirect("/buy")

# FIX ERROR HANDLING
@app.route("/submit/sell", methods=["POST"])
def submit_sell():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    tx_details = {}

    tx_details["datetime"] = request.form["datetime"]
    tx_details["ticker"] = request.form["ticker"]
    tx_details["amount"] = request.form["amount"]
    tx_details["price"] = request.form["price"]
    tx_details["note"] = request.form["note"]
    tx_details["user_id"] = session["user_id"]

    sql.submit_tx(tx_details, "sell")

    return redirect("/sell")

# FIX ERROR HANDLING
@app.route("/submit/feedback", methods=["POST"])
def submit_feedback():
    name = request.form["name"]
    message = request.form["message"]

    if len(name) > 100:
        return render_template("error.html", error="The name is too long")
    if len(message) > 5000:
        return render_template("error.html", error="The message is too long")

    sql.submit_feedback(name, message)

    return redirect("/")

@app.route("/transactions")
def transactions():
    user_id = session["user_id"]
    transactions = sql.fifo(user_id)

    return render_template("transactions.html", transactions=transactions)
