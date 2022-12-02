from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from fifo_sql import fifo_sql
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") #.replace("://", "ql://", 1)
app.secret_key = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)

user_id = 1

@app.route("/")
def index():
    return render_template("index.html")

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
    fee = request.form["fee"]
    note = request.form["note"]

    sql = "INSERT INTO tx (user_id, datetime, ticker, " \
        "amount, price, fee, note) VALUES (:user_id, :datetime, " \
        ":ticker, :amount, :price, :fee, :note)"

    db.session.execute(sql, {"user_id":user_id,
        "datetime":datetime, "ticker":ticker, "amount":amount, 
        "price":price, "fee":fee, "note":note})

    db.session.commit()

    return redirect("/buy")

@app.route("/submit/sell", methods=["POST"])
def submit_sell():

    datetime = request.form["datetime"]
    ticker = request.form["ticker"]
    amount = request.form["amount"]
    price = request.form["price"]
    fee = request.form["fee"]
    note = request.form["note"]

    sql = "INSERT INTO tx (user_id, datetime, ticker, " \
        "amount, price, fee, note) VALUES (:user_id, :datetime, " \
        ":ticker, :amount, :price, :fee, :note)"

    db.session.execute(sql, {"user_id":user_id,
        "datetime":datetime, "ticker":ticker, "amount":f"-{amount}", 
        "price":price, "fee":fee, "note":note})

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
    
    db.session.execute(sql, {"name":name, "message":message})
    db.session.commit()

    return redirect("/")

@app.route("/transactions")
def transactions():
    result = db.session.execute(fifo_sql, {"user_id":user_id})
    transactions = result.fetchall()

    return render_template("transactions.html", transactions=transactions)

