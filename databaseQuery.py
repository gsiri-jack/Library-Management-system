import bcrypt
from pymysql import Error
from mysqlCon import MySQLConnection
import json
from datetime import datetime, timedelta


with open("bookdata.json", "r") as file:
    data = json.load(file)


class services:
    def __init__(self):
        self.db_connection = MySQLConnection()
        self.db_connection.connect()

    def verify_user(self, user_id, password):
        query = "SELECT password FROM users_table WHERE user_id = %s"
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            stored_password = result[0]['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                print("Password is correct")
                print("User authenticated successfully")
                return True
            else:
                print("Password is incorrect")
                print("User authentication failed")
                return False
        else:
            print("User not found")
            return False

    def search_book(self, title=None, author=None, genre=None, isbn=None):
        query = "SELECT * FROM book_table WHERE 1=1"
        params = []
        if title:
            query += " AND title LIKE %s"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE %s"
            params.append(f"%{author}%")
        if genre:
            query += " AND genre LIKE %s"
            params.append(f"%{genre}%")
        if isbn:
            query += " AND isbn = %s"
            params.append(isbn)

        results = self.db_connection.fetch_results(query, params)
        print("Search Results:", results)
        return results


class librarian(services):
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

    def create_user(self, user_id, username, password, user_type):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), salt).decode('utf-8')
        print(f"Hashed Password: {hashed_password}")
        print(f"Salt: {salt.decode('utf-8')}")
        query = """
        INSERT INTO users_table (user_id, username, password, user_type)
        VALUES (%s, %s, %s, %s)
        """
        params = (user_id, username, hashed_password, user_type)
        try:
            self.db_connection.execute_query(query, params)
            print("User created successfully")
        except Error as e:
            print(f"Error: {e}")

    def issue_book(self, user_id, book_id):
        query = "SELECT issue_id, user_id, book_id FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)

        if result:
            print("Book already issued")
        else:
            issue_date = datetime.now()
            return_date = issue_date + timedelta(days=14)
            temp = self.db_connection.fetch_results(
                "SELECT issue_id FROM issues_table")
            if temp is None:
                self.db_connection.execute_query(
                    "ALTER TABLE issues_table AUTO_INCREMENT = 1000")

            query = """
            INSERT INTO issues_table (user_id, book_id, issue_date, return_date)
            VALUES (%s, %s, %s, %s)
            """
            params = (user_id, book_id, issue_date, return_date)
            try:
                self.db_connection.execute_query(query, params)
                print("Book issued successfully")
            except Error as e:
                print(f"Error: {e}")

    def return_book(self, user_id, book_id):
        query = """
        SELECT issue_id FROM issues_table WHERE user_id = %s AND book_id = %s
        """
        params = (user_id, book_id)
        try:
            issue_id = self.db_connection.fetch_results(query, params)
        except Error as e:
            print(f"Error: {e}")

        if issue_id:
            query = "DELETE FROM issues_table WHERE issue_id = %s"
            params = (issue_id[0]['issue_id'],)
            self.db_connection.execute_query(query, params)
            print("Book returned successfully")
        else:
            print("No record found for this issue")


class student(services):
    def __init__(self):
        self.db_connection = MySQLConnection()
        self.db_connection.connect()

    def view_shelf(self, user_id, *args):
        query = """SELECT * FROM issues_table WHERE user_id = %s"""
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            query = """SELECT username FROM users_table WHERE user_id = %s"""
            params = (user_id,)
            user_name = self.db_connection.fetch_results(query, params)[
                0]['username']

            print("The shelf of user:", user_name)
            self.book_id = result[0]['book_id']
            query = """SELECT * FROM book_table WHERE book_id = %s"""
            params = (self.book_id,)
            result = self.db_connection.fetch_results(query, params)
            print("Book name:", result[0]['title'])
            print("Book author:", result[0]['author'])
        else:
            print("Empty shelf")

    def reserve_book(self, user_id, book_id, *args):
        query = "SELECT reserve_id, user_id, book_id FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)

        if result:
            print("Book already reserved")
        else:
            reserve_date = datetime.now()
            # return_date = issue_date + timedelta(days=14)
            temp = self.db_connection.fetch_results(
                "SELECT reserve_id FROM issues_table")
            if temp is None:
                self.db_connection.execute_query(
                    "ALTER TABLE issues_table AUTO_INCREMENT = 9999")

            query = """
            INSERT INTO reserveBooks (reserve_id, book_id, issue_date, return_date)
            VALUES (%s, %s, %s, %s)
            """
            params = (user_id, book_id, issue_date, return_date)
            try:
                self.db_connection.execute_query(query, params)
                print("Book issued successfully")
            except Error as e:
                print(f"Error: {e}")
