import pymysql
from pymysql import Error
from mysqlCon import MySQLConnection
import json


db_connection = MySQLConnection()
db_connection.connect()
with open("bookdata.json", "r") as file:
    data = json.load(file)


db_connection.disconnect()
