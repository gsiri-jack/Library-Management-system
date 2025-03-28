import pymysql
from pymysql import Error
from mysqlCon import MySQLConnection
import json


with open("bookdata.json", "r") as file:
    data = json.load(file)


class Book:
    def __init__(self):
        self.db_connection = MySQLConnection()
        self.db_connection.connect()

    def insert_book(self, title, author, genre, isbn, publisher, published_year, pages):
        query = """
        INSERT INTO book_table (title, author, genre, isbn, publisher, published_year, pages)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, author, genre, isbn, publisher, published_year, pages)
        self.db_connection.execute_query(query, params)

    def remove_book(self, book_id):
        query = "DELETE FROM book_table WHERE book_id = %s"
        params = (book_id,)
        self.db_connection.execute_query(query, params)
