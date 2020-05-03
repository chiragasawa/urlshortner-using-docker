import pymysql
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint

class Database:
    def __init__(self,dbase):
        host = "dbos"
        user = "root"
        password = "jakaas"
        db = dbase
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        print("connected")
    def create_table(self):
        try:
            self.cur.execute("use url_short;")
            self.cur.execute("""
            create table website_url(
            website varchar(500) not null ,
            short_url varchar(255) primary key not null,
            dtype varchar(10) not null
            );""")
            self.con.commit()
        finally:
            self.con.close()


    def list_employees(self):
        self.cur.execute("select * from website_url;")
        result = self.cur.fetchall()
        return result
    def insert_data(self,website,short,dtype):
        try:
            print("here",website,short)
            self.cur.execute("""INSERT INTO website_url (website,short_url,dtype) VALUES (%s,%s,%s)""",(website,short,dtype ))
            self.con.commit()
            print("value inseted")
            return "done"
        except pymysql.Error as e:
            print("error in insert_data function demodb.",e)
            return "fail"
        finally:
            self.con.close()
            print("connection closed")
    def findrow(self,short):
        try:
            self.cur.execute("""select website,dtype from website_url where short_url=%s;""",(short))
            result = self.cur.fetchone()
            print(result)
            print("value fecthced")
            return result
        except pymysql.Error as e:
             print("error in findrow function demodb.",e)
        finally:
            self.con.close()
