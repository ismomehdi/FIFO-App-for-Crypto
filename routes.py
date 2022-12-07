from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from db.fifo_sql import fifo_sql
import secrets


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
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


@app.route("/submit/signup", methods=["POST"])
def submit_signup():

    username = request.form["username"]
    pwd_hash = generate_password_hash(request.form["password"])

    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"

    db.session.execute(sql, {"username": username, "password": pwd_hash})
    db.session.commit()

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


@app.route("/submit/buy", methods=["POST"])
def submit_buy():

    datetime = request.form["datetime"]
    ticker = request.form["ticker"]
    amount = request.form["amount"]
    price = request.form["price"]
    note = request.form["note"]

    user_id = session["user_id"]

    sql = "INSERT INTO tx (user_id, datetime, ticker, " \
        "amount, price, note) VALUES (:user_id, :datetime, " \
        ":ticker, :amount, :price, :note)"

    db.session.execute(sql, {"user_id": user_id,
                             "datetime": datetime, "ticker": ticker, "amount": amount,
                             "price": price, "note": note})

    db.session.commit()

    return redirect("/buy")


@app.route("/submit/sell", methods=["POST"])
def submit_sell():

    datetime = request.form["datetime"]
    ticker = request.form["ticker"]
    amount = request.form["amount"]
    price = request.form["price"]
    note = request.form["note"]

    user_id = session["user_id"]

    sql = "INSERT INTO tx (user_id, datetime, ticker, " \
        "amount, price, note) VALUES (:user_id, :datetime, " \
        ":ticker, :amount, :price, :note)"

    db.session.execute(sql, {"user_id": user_id,
                             "datetime": datetime, "ticker": ticker, "amount": f"-{amount}",
                             "price": price, "note": note})

    db.session.commit()

    return redirect("/sell")


@app.route("/submit/feedback", methods=["POST"])
def submit_feedback():
    name = request.form["name"]
    message = request.form["message"]

    if len(name) > 100:
        return render_template("error.html", error="The name is too long")
    if len(message) > 5000:
        return render_template("error.html", error="The message is too long")

    sql = "INSERT INTO feedback (name, message)"  \
        "VALUES (:name, :message)"

    db.session.execute(sql, {"name": name, "message": message})
    db.session.commit()

    return redirect("/")


@app.route("/transactions")
def transactions():
    user_id = session["user_id"]
    result = db.session.execute(fifo_sql, {"user_id": user_id})
    transactions = result.fetchall()

    return render_template("transactions.html", transactions=transactions)
