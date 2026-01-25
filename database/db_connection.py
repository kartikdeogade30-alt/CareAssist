import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="careassist.c25yw2e4gjvz.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Dbda#1234",
        database="careassist",
        port="3306",
        autocommit=False
    )