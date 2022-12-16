from services.sql_tool import SQLTool


class Query:
    def __init__(self, db):
        self.db = db
        self.sql = SQLTool(db)

    def get_transaction_history(self, portfolio_id):
        path = 'db/queries/get_transaction_history.sql'
        args = {'portfolio_id': portfolio_id}
        result = self.sql.fetch_all(path, args)

        return result

    def get_login_credentials(self, username):
        path = 'db/queries/get_login_credentials.sql'
        args = {'username': username}
        result = self.sql.fetch_one(path, args)

        return result

    def portfolio_count(self, user_id):
        path = 'db/queries/portfolio_count.sql'
        args = {'user_id': user_id}
        result = self.sql.fetch_one(path, args)

        return result

    def get_default_portfolio(self, user_id):
        path = 'db/queries/get_default_portfolio.sql'
        args = {'user_id': user_id}
        result = self.sql.fetch_one(path, args)

        return result

    def username_exists(self, username):
        path = 'db/queries/get_username.sql'
        args = {"username": username}
        result = self.sql.fetch_one(path, args)

        if result is None:
            return False

        return True

    def signup(self, username, pwd_hash):
        path = 'db/queries/create_user.sql'
        args = {"username": username, "password": pwd_hash}
        execute = self.sql.execute(path, args)

    def submit_tx(self, tx_dict):
        path = 'db/queries/create_transaction.sql'
        args = tx_dict
        execute = self.sql.execute(path, args)

    def submit_feedback(self, name, message):
        path = 'db/queries/submit_feedback.sql'
        args = {"name": name, "message": message}
        execute = self.sql.execute(path, args)
