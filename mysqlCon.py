import pymysql
import json
from pymysql import Error


class MySQLConnection:
    def __init__(self):
        self.host = "libs-mang-pace-a6bb.h.aivencloud.com"
        self.port = 11632
        self.cursorclass = pymysql.cursors.DictCursor
        self.charset = "utf8mb4"
        self.connect_timeout = 10
        self.read_timeout = 10
        self.user = "avnadmin"
        self.password = "AVNS_kJAYQ8B-B72d_qVa0lR"
        self.database = "jack"
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                cursorclass=self.cursorclass,
                write_timeout=self.connect_timeout,
            )
            # if self.connection:
            #     # print("Connection to MySQL database successful")
            #     return True
        except Error as e:
            # print(f"Error: {e}")
            self.connection = None
            return e

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("MySQL connection closed")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("No active database connection")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: {e}")

    def fetch_results(self, query, params=None):
        if not self.connection:
            print("No active database connection")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
