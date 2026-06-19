from Models.DB import DB

class AdminDAO:
    def __init__(self, db: DB):
        self.db = db

    def getByEmail(self, email):
        q = self.db.query("select * from admin where email='{}'".format(email))
        return q.fetchone()

    def getById(self, id):
        q = self.db.query("select * from admin where id='{}'".format(id))
        return q.fetchone()
