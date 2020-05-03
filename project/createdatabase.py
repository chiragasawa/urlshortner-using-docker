import pymysql

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "jakaas"
        db = "None"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        print("connected")
    def create_table(self):
        print("helloworld")
if __name__ == "__main__":
    db=Database()
    db.create_table();
            

