from databaseQuery import librarian, student, services

# Initialize the services
service = services()

# Verify the user
verify_user, user_m = service.verify_user(
    user_id="admin",  # Replace with the actual user ID
    password="password"  # Replace with the actual password
)


class admin_panel():
    def __init__(self, is_verified, user_type):
        if not is_verified or user_type != "admin":
            raise PermissionError(
                "Access denied: Only admin users can access the admin panel.")
        self.admin = librarian()
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type

    def create_user(self):
        user_id = input("Enter user ID: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_type = input("Enter user type (admin/student): ")
        success, message = self.admin.create_user(
            user_id=user_id,
            username=username,
            password=password,
            user_type=user_type
        )
        print(message)

    def insert_book(self):
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        genre = input("Enter genre: ")
        isbn = input("Enter ISBN: ")
        publisher = input("Enter publisher: ")
        published_year = int(input("Enter published year: "))
        pages = int(input("Enter number of pages: "))
        success, message = self.admin.insert_book(
            title=title,
            author=author,
            genre=genre,
            isbn=isbn,
            publisher=publisher,
            published_year=published_year,
            pages=pages
        )
        print(message)


class student_panel():
    def __init__(self, is_verified, user_type):
        if not is_verified or user_type != "student":
            raise PermissionError(
                "Access denied: Only student users can access the student panel.")
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type

    def view_shelf(self):
        user_id = input("Enter your user ID: ")
        success, message = self.student.view_shelf(user_id=user_id)
        if success:
            print("Shelf details:", message)
        else:
            print(message)


# Display the dashboard menu based on the user type
if verify_user:
    if user_m == "admin":
        dashboard = admin_panel(
            is_verified=service.is_verified, user_type=service.user_type)
        while True:
            print("\nAdmin Dashboard")
            print("1. Create User")
            print("2. Insert Book")
            print("3. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                dashboard.create_user()
            elif choice == "2":
                dashboard.insert_book()
            elif choice == "3":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    elif user_m == "student":
        dashboard = student_panel(
            is_verified=service.is_verified, user_type=service.user_type)
        while True:
            print("\nStudent Dashboard")
            print("1. View Shelf")
            print("2. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                dashboard.view_shelf()
            elif choice == "2":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("User type not recognized")
else:
    print(user_m)
