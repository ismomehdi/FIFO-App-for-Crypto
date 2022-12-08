class SQLQuery:
    def __init__(self, db):
        self.db = db

    def fifo(self, user_id):
        # Calculate FIFO PnL for each sell transaction

        sql = """
        SELECT
            tx_view.id,
            tx_view.datetime,
            tx_view.ticker,
            tx_view.amount,
            tx_view.price,
            tx_view.fee,
            tx_view.note,
            tx_view.type,
            sell_stats_view.total_pnl
        FROM
            tx_view
        LEFT JOIN 
            sell_stats_view
        ON 
            tx_view.id = sell_stats_view.id
        WHERE
            tx_view.user_id = :user_id
        ORDER BY 
            datetime, tx_view.id;
        """

        result = self.db.session.execute(sql, {"user_id": user_id})
        transactions = result.fetchall()

        return transactions

    def login(self, username):
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()

        return user

    def signup(self, username, pwd_hash):
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        self.db.session.execute(sql, {"username": username, "password": pwd_hash})
        self.db.session.commit()

    def submit_tx(self, tx_details, tx_type):
        user_id = tx_details["user_id"]
        datetime = tx_details["datetime"]
        ticker = tx_details["ticker"]
        price = tx_details["price"]
        note = tx_details["note"]

        if tx_type == "sell":
            amount = f"-{tx_details['amount']}"
        else:
            amount = tx_details["amount"]


        sql = "INSERT INTO tx (user_id, datetime, ticker, " \
            "amount, price, note) VALUES (:user_id, :datetime, " \
            ":ticker, :amount, :price, :note)"

        self.db.session.execute(sql, {"user_id": user_id,
                                "datetime": datetime, "ticker": ticker, "amount": amount,
                                "price": price, "note": note})

        self.db.session.commit()

    def submit_feedback(self, name, message):
        sql = "INSERT INTO feedback (name, message) VALUES (:name, :message)"
        self.db.session.execute(sql, {"name": name, "message": message})
        self.db.session.commit()
    
    