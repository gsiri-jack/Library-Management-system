import bcrypt
from pymysql import Error
from mysqlCon import MySQLConnection
import json
from datetime import datetime, timedelta
from functools import wraps

# Load book data from JSON file
with open("bookdata.json", "r") as file:
    data = json.load(file)


def require_verification(func):
    """Decorator to ensure the user is verified before performing any operation."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_verified:
            return False, "Access denied: User is not verified."
        return func(self, *args, **kwargs)
    return wrapper


def admin_only(func):
    """Decorator to restrict access to admin-only methods."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.user_type != "admin":
            return False, f"Access denied: Only admin users can perform this operation.{self.user_type}"
        return func(self, *args, **kwargs)
    return wrapper


class services:
    def __init__(self):
        self.db_connection = MySQLConnection()
        self.db_connection.connect()
        self.is_verified = False
        self.user_type = None

    def verify_user(self, user_id, password):
        query = "SELECT password, user_type FROM users_table WHERE user_id = %s"
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            stored_password = result[0]['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                self.is_verified = True
                self.user_type = result[0]['user_type']
                return True, self.user_type
            else:
                return False, "Password is incorrect."
        else:
            return False, "User not found."

    def logout(self):
        """Logs out the user by resetting verification and user type."""
        self.is_verified = False
        self.user_type = None
        return True, "User has been logged out successfully."

    # @require_verification
    def search_book(self, book_id=None, title=None, author=None, genre=None, isbn=None):
        query = "SELECT * FROM book_table WHERE 1=1"
        params = []
        if book_id:
            query += " AND book_id = %s"
            params.append(book_id)
        if title:
            query += " AND  LOWER(title) LIKE LOWER(%s)"
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
        if results:
            return True, results
        return False, "No books found."

    def search_book_by_title(self, title):
        # Split the title into words and construct the LIKE clauses
        like_clauses = " OR ".join([
            "LOWER(title) LIKE %s" for _ in title.split()
        ])
        params = [f"%{word.lower()}%" for word in title.split()
                  ]  # Ensure case-insensitivity
        query = f"SELECT * FROM book_table WHERE {like_clauses}"

        # Execute the query and fetch results
        results = self.db_connection.fetch_results(query, params)
        if results:
            return True, results
        return False, "No books found."

    def get_book_details(self, key_name, key_value, columnName):
        # Define allowed column names
        allowed_keys = {"book_id", "image_id", "isbn"}
        if key_name not in allowed_keys:
            return False, "Invalid key name."

        query = f"SELECT {columnName} FROM book_table WHERE {key_name} = %s"
        params = (key_value,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            if columnName == '*':
                return True, result[0]
            else:
                return True, result[0][columnName]
        return False, "Book not found."

    def check_book_issued(self, book_id):
        query = "SELECT issue_id FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            return True, "Book is issued."
        return False, "Book is not issued."

    def calculate_fine(self, book_id):
        query = "SELECT issue_date, return_date FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)
        print(result)
        if result:
            issue_date = result[0]['issue_date']
            return_date = result[0]['return_date']
            current_date = datetime.now()

            if current_date < return_date:
                overdue_days = (abs(current_date - return_date)).days
                fine_amount = overdue_days * 5
                return True, fine_amount
            else:
                return False, "Book is not overdue."
        return False, "Book not found."

    def get_user_details(self, user_id):
        query = "SELECT username FROM users_table WHERE user_id = %s"
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            return True, result[0]['username']
        return False, "User not found."


class librarian(services):
    # @admin_only
    # @require_verification

    def insert_book(self, title, author, genre, isbn, publisher, published_year, pages, image_id):
        query = """
        INSERT INTO book_table (title, author, genre, isbn, publisher, published_year, pages,image_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, author, genre, isbn, publisher,
                  published_year, pages, image_id)
        try:
            self.db_connection.execute_query(query, params)
        except Error as e:
            return False, f"Error inserting book: {e}"

        book_id = self.get_book_details("isbn", isbn, "book_id")
        if book_id[0]:
            book_id = book_id[1]
            return True, book_id

    # @admin_only
    # @require_verification
    def remove_book(self, book_id):
        title = self.get_book_details("book_id", book_id, "title")
        query = "DELETE FROM book_table WHERE book_id = %s"
        params = (book_id,)
        try:
            self.db_connection.execute_query(query, params)
            return True, title[1]
        except Error as e:
            return False, f"Error removing book: {e}"

    # @admin_only
    # @require_verification
    def create_user(self, user_id, username, password, user_type):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), salt).decode('utf-8')
        query = """
        INSERT INTO users_table (user_id, username, password, user_type)
        VALUES (%s, %s, %s, %s)
        """
        params = (user_id, username, hashed_password, user_type)
        try:
            self.db_connection.execute_query(query, params)
            return True, "User created successfully."
        except Error as e:
            return False, f"Error creating user: {e}"

    # @admin_only
    # @require_verification
    def issue_book(self, user_id, book_id, days=14):
        try:
            # Ensure book_id is an integer
            book_id = int(book_id)
        except ValueError:
            return False, f"Invalid book ID. It must be a numeric value.{book_id}"

        query = "SELECT issue_id FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)

        if result:
            return False, "Book already issued."
        else:
            issue_date = datetime.now()
            return_date = issue_date + timedelta(days=days)

            temp = self.db_connection.fetch_results(
                "SELECT issue_id FROM issues_table")
            if not temp:
                self.db_connection.execute_query(
                    "ALTER TABLE issues_table AUTO_INCREMENT = 1000")

            query = """
            INSERT INTO issues_table (user_id, book_id, issue_date, return_date)
            VALUES (%s, %s, %s, %s)
            """
            params = (user_id, book_id, issue_date, return_date)
            try:
                self.db_connection.execute_query(query, params)
                return True, "Book issued successfully."
            except Error as e:
                return False, f"Error issuing book: {e}"

    def get_issued_book_details(self, book_id):
        query = "SELECT * FROM issues_table WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            issue_date = result[0]['issue_date']
            return_date = result[0]['return_date']
            user_id = result[0]['user_id']
            username = self.get_user_details(user_id)[1]

            book_title = self.get_book_details("book_id", book_id, "title")[1]

            return True, {
                "book_id": book_id,
                "issue_date": issue_date,
                "return_date": return_date,
                "user_id": user_id,
                "username": username,
                "title": book_title
            }
        return False, "No issued book found."

    # @admin_only
    # @require_verification
    def return_book(self, user_id, book_id):
        query = """
        SELECT issue_id FROM issues_table WHERE user_id = %s AND book_id = %s
        """
        params = (user_id, book_id)
        try:
            issue_id = self.db_connection.fetch_results(query, params)
        except Error as e:
            return False, f"Error fetching issue record: {e}"

        if issue_id:
            query = "DELETE FROM issues_table WHERE issue_id = %s"
            params = (issue_id[0]['issue_id'],)
            try:
                self.db_connection.execute_query(query, params)
                return True, "Book returned successfully."
            except Error as e:
                return False, f"Error returning book: {e}"
        else:
            return False, "No record found for this issue."

    def get_student_details_by_username(self, username):
        query = "SELECT user_id, username, user_type FROM users_table WHERE username = %s"
        params = (username,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            return True, result
        return False, "User not found."

    def get_all_users(self):
        query = "SELECT user_id, username, user_type FROM users_table WHERE user_type = 'student'"
        result = self.db_connection.fetch_results(query)
        if result:
            return True, result
        return False, "No users found."


class student(services):
    def __init__(self):
        self.db_connection = MySQLConnection()
        self.db_connection.connect()
    # #@require_verification

    def view_shelf(self, user_id, *args):
        query = """SELECT * FROM issues_table WHERE user_id = %s"""
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            query = """SELECT COUNT(*) AS count FROM issues_table WHERE user_id = %s"""
            params = (user_id,)
            book_count = self.db_connection.fetch_results(query, params)[
                0]['count']

            return True, {
                "book_count": book_count,
                "book_details": result
            }
        return False, "Empty shelf."

    def issued_books_table(self, user_id):
        self.user_id = user_id
        res = self.view_shelf(self.user_id)
        if res[0]:
            shelf = []
            for i in range(res[1]['book_count']):
                val = res[1]['book_details'][i]
                book_id = val['book_id']
                title = self.get_book_details(book_id, 'title')
                issue_date = val['issue_date']
                return_date = val['return_date']
                shelf.append({
                    "book_id": book_id,
                    "title": title,
                    "issue_date": issue_date,
                    "return_date": return_date
                })

            return True, res[1]['book_count'], shelf
        return False, "No issued books found."

    # @require_verification

    def reserve_book(self, user_id, book_id, *args):
        query = "SELECT reserve_id FROM reserveBooks WHERE book_id = %s"
        params = (book_id,)
        result = self.db_connection.fetch_results(query, params)
        # print(result)

        if result:
            return False, "Book already reserved."
        else:
            reserve_date = datetime.now()
            # print(reserve_date)

            temp = self.db_connection.fetch_results(
                "SELECT reserve_id FROM reserveBooks")
            # print(temp)
            if len(temp) == 0:
                self.db_connection.execute_query(
                    "ALTER TABLE reserveBooks AUTO_INCREMENT = 1111")

            query = """
            INSERT INTO reserveBooks (user_id, book_id, reserve_date)
            VALUES (%s, %s, %s)
            """
            params = (user_id, book_id, reserve_date)
            try:
                self.db_connection.execute_query(query, params)
                print("Book reserved successfully.")
                return True, "Book reserved successfully."
            except Error as e:
                return False, f"Error reserving book: {e}"

    # #@require_verification
    def get_reserve_books(self, user_id):
        query = "SELECT * FROM reserveBooks WHERE user_id = %s"
        params = (user_id,)
        result = self.db_connection.fetch_results(query, params)
        if result:
            return True, result
        return False, "No reserved books found."

    # @require_verification
