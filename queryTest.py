from databaseQuery import librarian, student

staff = librarian()
stu = student()
# book = Book.insert_book(
#     title="Sample Book",
#     author="John Doe",
#     genre="Fiction",
#     isbn="123456789",
#     publisher="Sample Publisher",
#     published_year=2023,
#     pages=300
# )


staff.verify_user(
    user_id="sample_user_id2",
    password="sample_password2"
)

staff.search_book(
    genre="gothic",
)

# query = """ """
# staff.db_connection.execute_query(query)

# # Set the starting value for AUTO_INCREMENT (optional)
# staff.db_connection.execute_query("")

# Set the starting value for AUTO_INCREMENT (optional)
# staff.db_connection.execute_query(
#     "ALTER TABLE issues_table AUTO_INCREMENT = 1000")
staff.issue_book(
    user_id="student_user_id2",
    book_id=1
)


# stu.verify_user(
#     user_id="student_user_id2",
#     password="student_password2"
# )

stu.view_shelf(
    user_id="student_user_id2",
)

query = """CREATE TABLE IF NOT EXISTS reserveBooks(resrve_id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), book_id INT, reserve_date DATETIME)"""
staff.db_connection.execute_query(query)
