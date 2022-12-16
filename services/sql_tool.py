class SQLTool:
    def __init__(self, db):
        self.db = db

    def read_file(self, path: str):
        with open(path, "r") as file:
            sql = file.read()
        
        return sql

    def fetch_one(self, path: str, args: dict):
        query = self.read_file(path)
        result = self.db.session.execute(query, args)
        result = result.fetchone()
        result = self.extract_if_single_value(result)

        return result

    def fetch_all(self, path: str, args: dict):
        query = self.read_file(path)
        result = self.db.session.execute(query, args)
        result = result.fetchall()

        return [dict(r) for r in result]
    
    def execute(self, path: str, args: dict):
        query = self.read_file(path)

        try:
            self.db.session.execute(query, args)
            self.db.session.commit()
        except:
            raise Exception("Oops, error executing query.")

    def extract_if_single_value(self, result: object):
        if result is not None:
            if len(result) == 1:
                return result[0]

        return result
        
