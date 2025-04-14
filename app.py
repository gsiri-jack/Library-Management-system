import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from databaseQuery import librarian, student, services
from PIL import Image
from random import randint
import threading
import time


class LibraryManagement(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("700x700")
        ctk.set_appearance_mode("Dark")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # self.show_login()
        self.login()

    def show_login(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.container)
        frame.pack(expand=True)

        label = ctk.CTkLabel(frame, text="Login", font=("Arial", 20))
        label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(
            frame, placeholder_text="Password", show="•")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(frame, text="Login", command=self.login)
        login_button.pack(pady=10)

    def login(self):

        # For testing purposes

        self.user_id = "prime"
        self.password = 'prime'

        service = services()
        verify_user, user_type = service.verify_user(
            user_id=self.user_id,
            password=self.password
        )

        if verify_user:
            if user_type == 'admin':
                self.show_admin_panel()
            elif user_type == 'student':
                self.show_student_panel()
            else:
                messagebox.showerror("Error", "Invalid user type!")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_admin_panel(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        self.admin_panel = admin_panel(
            self.container, self, self.user_id, is_verified=True, user_type="admin")
        self.admin_panel.pack(fill="both", expand=True)

    def reset_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_student_panel(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        self.student_panel = student_panel(
            self.container, self, self.user_id, is_verified=True, user_type="student")
        self.student_panel.pack(fill="both", expand=True)


class admin_panel(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.admin = librarian()
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.admin.user_id = user_id
        self.user_id = user_id

        # Initialize view_students_frame to None
        self.view_students_frame = None
        self.add_book_frame = None
        self.remove_book_frame = None
        self.issue_book_frame = None
        self.return_book_frame = None
        self.add_student_frame = None

        self.label = ctk.CTkLabel(self, text="Admin Panel", font=("Arial", 20))
        # Changed from pack to grid
        self.label.grid(row=0, column=1, sticky="n")
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=9, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')

        self.menu = admin_menu(
            self, app, user_id, is_verified, user_type)
        self.menu.grid(row=0, column=0, sticky="nsew")

        self.admin_dashboard = admin_dashboard(
            self, self.app, self.user_id, None, self.admin.is_verified, self.admin.user_type)
        self.admin_dashboard.grid(row=0, column=1, sticky="nsew")

    def show_admin_dashboard(self):
        self.admin_dashboard.tkraise()

    def view_students(self):
        if (self.view_students_frame != None):
            self.view_students_frame.destroy()
        self.view_students_frame = view_students_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.view_students_frame.grid(row=0, column=1, sticky="nsew")
        print(self.view_students_frame)

    def add_book_dashboard(self):
        if (self.add_book_frame != None):
            self.add_book_frame.destroy()
        self.add_book_frame = add_book_frame(
            self, self.app, self.admin, self.user_id, is_verified=True, user_type="admin")
        self.add_book_frame.grid(row=0, column=1, sticky="nsew")
        print(self.add_book_frame)

    def remove_book_dashboard(self):
        if (self.remove_book_frame != None):
            self.remove_book_frame.destroy()
        self.remove_book_frame = remove_book_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.remove_book_frame.grid(row=0, column=1, sticky="nsew")
        print(self.remove_book_frame)

    def issue_book_dashboard(self):
        if (self.issue_book_frame != None):
            self.issue_book_frame.destroy()
        self.issue_book_frame = issue_book_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.issue_book_frame.grid(row=0, column=1, sticky="nsew")
        print(self.issue_book_frame)

    def return_book_dashboard(self):
        if (self.return_book_frame != None):
            self.return_book_frame.destroy()
        self.return_book_frame = return_book_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.return_book_frame.grid(row=0, column=1, sticky="nsew")
        print(self.return_book_frame)

    def add_student_dashboard(self):
        if (self.add_student_frame != None):
            self.add_student_frame.destroy()
        self.add_student_frame = add_student_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.add_student_frame.grid(row=0, column=1, sticky="nsew")
        print(self.add_student_frame)

    def show_admin_dashboard(self):
        if (self.admin_dashboard != None):
            self.admin_dashboard.destroy()
        self.admin_dashboard = add_student_frame(
            self, self.app, self.user_id, is_verified=True, user_type="admin")
        self.admin_dashboard.grid(row=0, column=1, sticky="nsew")
        print(self.admin_dashboard)

    def reset_frame(self, master):
        pass

    def logout(self):
        self.admin.is_verified = False
        self.admin.user_type = None
        self.app.show_login()


class view_students_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.admin = librarian()
        self.master.admin.is_verified = is_verified
        self.master.admin.user_type = user_type
        self.user_id = user_id

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=3, uniform='a')
        self.grid_rowconfigure(1, weight=6, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="View Students", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")

        self.search_bar = ctk.CTkEntry(
            self, placeholder_text="Search for books", width=400, height=50, )
        self.search_bar.grid(row=2, column=0, pady=10, sticky="n")

        self.search_button = ctk.CTkButton(
            self, text="Search", command=self.refresh_table_with_search)
        self.search_button.grid(row=2, column=0, padx=5, )

        # Create a Treeview widget to display student data
        self.style = ttk.Style(self)
        self.configure_style()
        self.table = ttk.Treeview(self, columns=(
            "Student ID", 'Name', 'Email', 'Phone'), show="headings")
        self.table.heading("Student ID", text="Student ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Email", text="Email")
        self.table.heading("Phone", text="Phone")

        # Configure column widths
        self.table.column("Student ID", width=100)
        self.table.column("Name", width=150)
        self.table.column("Email", width=150)
        self.table.column("Phone", width=100)

        # Populate the table with student data
        self.update_table(self.table)
        self.table.grid(row=1, column=0, padx=50, pady=20, sticky="ew")

    def configure_style(self):
        """Configures the dark theme for the Treeview"""
        self.style.theme_use("clam")  # Use 'clam' as the base theme

        # Treeview background, text color, and row height
        self.style.configure("Treeview",
                             background="#333333",
                             foreground="white",
                             rowheight=25,
                             fieldbackground="#333333")

        # Selected row color
        self.style.map("Treeview",
                       background=[("selected", "#555555")],
                       foreground=[("selected", "white")])

        # Heading styling
        self.style.configure("Treeview.Heading",
                             background="#444444",
                             foreground="white",)

    def reset_view_studetnts_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def refresh_table_with_search(self):
        """Refresh the table with student details based on the search query."""
        search_query = self.search_bar.get().strip()
        if search_query == '' or search_query == ' ':
            for row in self.table.get_children():
                self.table.delete(row)
            student_details = self.admin.get_all_users()
            if student_details[0]:
                student_details = student_details[1]
                for student in student_details:
                    self.table.insert("", "end", values=(
                        student['user_id'],
                        student['username'],
                        'gjack@g',
                        900,
                    ))
        # Clear existing table data
        else:
            for row in self.table.get_children():
                self.table.delete(row)

            # Fetch student details based on the search query
            student_details = self.admin.get_student_details_by_username(
                search_query)
            if student_details[0]:
                print(student_details)
                student_details = student_details[1]
                for student in student_details:
                    self.table.insert("", "end", values=(
                        student['user_id'],
                        student['username'],
                        'gjack@g',
                        900,

                    ))
            else:
                messagebox.showinfo(
                    "Info", "No student found with the given username.")

    def update_table(self, table):
        # search_query = self.search_bar.get().strip()
        for row in self.table.get_children():
            self.table.delete(row)
        student_details = self.admin.get_all_users()
        if student_details[0]:
            student_details = student_details[1]
            for student in student_details:
                self.table.insert("", "end", values=(
                    student['user_id'],
                    student['username'],
                    'gjack@g',
                    900,
                ))


class add_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, admin, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.admin = admin  # Use the injected admin instance
        self.user_id = userid

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(tuple(range(8)), weight=1, uniform='a')

        # Title
        self.title_label = ctk.CTkLabel(
            self, text="Title:", font=("Arial", 14))
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.title_entry = ctk.CTkEntry(
            self, placeholder_text="Enter book title")
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Author
        self.author_label = ctk.CTkLabel(
            self, text="Author:", font=("Arial", 14))
        self.author_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.author_entry = ctk.CTkEntry(
            self, placeholder_text="Enter author name")
        self.author_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # ISBN
        self.isbn_label = ctk.CTkLabel(self, text="ISBN:", font=("Arial", 14))
        self.isbn_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.isbn_entry = ctk.CTkEntry(self, placeholder_text="Enter ISBN")
        self.isbn_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Publisher
        self.publisher_label = ctk.CTkLabel(
            self, text="Publisher:", font=("Arial", 14))
        self.publisher_label.grid(
            row=3, column=0, padx=10, pady=10, sticky="e")
        self.publisher_entry = ctk.CTkEntry(
            self, placeholder_text="Enter publisher name")
        self.publisher_entry.grid(
            row=3, column=1, padx=10, pady=10, sticky="w")

        # Published Year
        self.published_year_label = ctk.CTkLabel(
            self, text="Published Year:", font=("Arial", 14))
        self.published_year_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="e")
        self.published_year_entry = ctk.CTkEntry(
            self, placeholder_text="Enter published year")
        self.published_year_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="w")

        # Genre
        self.genre_label = ctk.CTkLabel(
            self, text="Genre:", font=("Arial", 14))
        self.genre_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.genre_entry = ctk.CTkEntry(self, placeholder_text="Enter genre")
        self.genre_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Image ID
        self.image_id_label = ctk.CTkLabel(
            self, text="Image ID:", font=("Arial", 14))
        self.image_id_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.image_id_entry = ctk.CTkEntry(
            self, placeholder_text="Enter image ID")
        self.image_id_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Pages
        self.pages_label = ctk.CTkLabel(
            self, text="Pages:", font=("Arial", 14))
        self.pages_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.pages_entry = ctk.CTkEntry(
            self, placeholder_text="Enter number of pages")
        self.pages_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self, text="Add Book", command=self.add_book_to_database)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=20)

    def add_book_to_database(self):
        """Add the book to the database and show a status message."""
        book_details = {
            "title": self.title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "isbn": self.isbn_entry.get().strip(),
            "publisher": self.publisher_entry.get().strip(),
            "published_year": self.published_year_entry.get().strip(),
            "genre": self.genre_entry.get().strip(),
            "image_id": self.image_id_entry.get().strip(),
            "pages": self.pages_entry.get().strip(),
        }

        # Validate input
        if not all(book_details.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Add book to the database
        result = self.admin.insert_book(
            book_details['title'], book_details["author"], book_details['genre'],
            book_details["isbn"], book_details['publisher'], book_details['published_year'], book_details['pages'],
            book_details['image_id']
        )
        if result[0]:  # Assuming the method returns a tuple (success, message)
            messagebox.showinfo(
                "Success", f"Book added successfully!{result[1]}")
            # Clear the form
            for entry in [self.title_entry, self.author_entry, self.isbn_entry,
                          self.publisher_entry, self.published_year_entry,
                          self.genre_entry, self.image_id_entry, self.pages_entry]:
                entry.delete(0, "end")
        else:
            messagebox.showerror("Error", f"Failed to add book: {result[1]}")


class remove_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.master.admin.is_verified = is_verified
        self.master.admin.user_type = user_type
        self.user_id = userid

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(tuple(range(3)), weight=1, uniform='a')

        # Title Label
        self.label = ctk.CTkLabel(
            self, text="Remove Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # ISBN Entry
        self.isbn_label = ctk.CTkLabel(
            self, text="Enter Book Id:", font=("Arial", 14))
        self.isbn_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.isbn_entry = ctk.CTkEntry(
            self, placeholder_text="Enter Book Id of the book to remove")
        self.isbn_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Remove Button
        self.remove_button = ctk.CTkButton(
            self, text="Remove Book", command=self.remove_book_from_database, fg_color="red")
        self.remove_button.grid(row=2, column=0, columnspan=2, pady=20)

    def remove_book_from_database(self):
        """Prompt confirmation before removing the book."""
        book_id = self.isbn_entry.get().strip()

        if not book_id:
            messagebox.showerror("Error", "Book_id field cannot be empty!")
            return

        # Fetch book details to get the title
        book_details = self.master.admin.get_book_details(
            'book_id', book_id, 'title')
        if not book_details[0]:
            messagebox.showerror("Error", f"Book not found: {book_details[1]}")
            return

        book_title = book_details[1]

        # Show confirmation modal
        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove the book '{book_title}'?"
        )

        if confirm:
            result = self.master.admin.remove_book(book_id)
            if result[0]:
                messagebox.showinfo(
                    "Success", f"Book '{book_title}' removed successfully!")
                self.isbn_entry.delete(0, "end")
            else:
                messagebox.showerror(
                    "Error", f"Failed to remove book: {result[1]}")
        else:
            messagebox.showinfo("Cancelled", "Book removal cancelled.")


class issue_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.master.admin.is_verified = is_verified
        self.master.admin.user_type = user_type
        self.user_id = userid

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(tuple(range(7)), weight=1, uniform='a')

        # Title Label
        self.label = ctk.CTkLabel(
            self, text="Issue Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # Book ID Entry
        self.book_id_label = ctk.CTkLabel(
            self, text="Enter Book ID:", font=("Arial", 14))
        self.book_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.book_id_entry = ctk.CTkEntry(
            self, placeholder_text="Enter Book ID")
        self.book_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Number of Days Entry
        self.days_label = ctk.CTkLabel(
            self, text="Number of Days (Max 14):", font=("Arial", 14))
        self.days_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.days_entry = ctk.CTkEntry(
            self, placeholder_text="Enter number of days")
        self.days_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Get Details Button
        self.get_details_button = ctk.CTkButton(
            self, text="Get Details", command=self.get_book_details, fg_color="blue")
        self.get_details_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Book Details Section
        self.book_details_label = ctk.CTkLabel(
            self, text="Book Details:", font=("Arial", 16))
        self.book_details_label.grid(
            row=4, column=0, columnspan=2, pady=10, sticky="n")

        # Use a scrollable text box for better appearance and functionality
        self.book_details_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.book_details_frame.grid(
            row=5, column=0, rowspan=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.book_details_frame.grid_rowconfigure(0, weight=1)
        self.book_details_frame.grid_columnconfigure(0, weight=1)

        self.book_details_text = ctk.CTkTextbox(
            self.book_details_frame, wrap="word", font=("Arial", 14), height=350, width=300)
        self.book_details_text.grid(row=0,  column=0, sticky="ns")

        # Add a scrollbar for the text box
        # self.scrollbar = ctk.CTkScrollbar(
        #     self.book_details_frame, command=self.book_details_text.yview)
        # self.scrollbar.grid(row=0, column=1, sticky="ns")
        # self.book_details_text.configure(yscrollcommand=self.scrollbar.set)

        # Issue Button
        self.issue_button = ctk.CTkButton(
            self, text="Issue Book", command=self.issue_book, fg_color="green")
        self.issue_button.grid(row=7, column=0, columnspan=2, pady=20)

    def get_book_details(self):
        """Fetch and display book details based on the entered Book ID."""
        book_id = self.book_id_entry.get().strip()
        print(book_id)
        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty!")
            return

        # Fetch book details
        book_details = self.master.admin.get_book_details(
            'book_id', book_id, '*')
        if not book_details[0]:
            messagebox.showerror("Error", f"Book not found: {book_details[1]}")
            self.book_details_text.configure(text="")
            return
        print(book_details[1])
        # Display book details
        book = book_details[1]
        details = (
            f'Book ID: {book["book_id"]}\n'
            f"Title: {book['title']}\n"
            f"Author: {book['author']}\n"
            f"Genre: {book['genre']}\n"
            f"Publisher: {book['publisher']}\n"
            f"Published Year: {book['published_year']}\n"
            f"Pages: {book['pages']}\n"
            f"ISBN: {book['isbn']}\n"
            f"Status: {'Issued' if self.master.admin.check_book_issued(book_id)[0] else 'Available'}"
        )
        self.book_details_text.delete("1.0", "end")
        self.book_details_text.insert("1.0", details)

    def issue_book(self):
        """Handle the book issuing process."""

        book_id = self.book_id_entry.get().strip()
        days = self.days_entry.get().strip()
        print(book_id, days)
        if not book_id or not days:
            messagebox.showerror(
                "Error", "Both Book ID and Number of Days are required!")
            return

        if not days.isdigit() or int(days) > 14:
            messagebox.showerror(
                "Error", "Number of days must be a valid number and not exceed 14!")
            return

        # Check if the book is already issued
        if self.master.admin.check_book_issued(book_id)[0]:
            messagebox.showerror("Error", "This book is already issued!")
            return

        # Issue the book
        result = self.master.admin.issue_book(self.user_id, book_id, int(days))
        if result[0]:
            messagebox.showinfo(
                "Success", f"Book issued successfully for {days} days!")
            self.book_id_entry.delete(0, "end")
            self.days_entry.delete(0, "end")
            self.book_details_text.configure(text="")
        else:
            messagebox.showerror("Error", f"Failed to issue book: {result[1]}")


class return_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.master.admin.is_verified = is_verified
        self.master.admin.user_type = user_type
        self.user_id = userid

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(tuple(range(9)), weight=1, uniform='a')

        # Title Label
        self.label = ctk.CTkLabel(
            self, text="Return Book", font=("Arial", 24, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # Book ID Entry
        self.book_id_label = ctk.CTkLabel(
            self, text="Enter Book ID:", font=("Arial", 16))
        self.book_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.book_id_entry = ctk.CTkEntry(
            self, placeholder_text="Enter Book ID", width=300)
        self.book_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Fetch Details Button
        self.fetch_button = ctk.CTkButton(
            self, text="Go", command=self.fetch_book_details, fg_color="blue")
        self.fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Book Details Section
        self.book_details_label = ctk.CTkLabel(
            self, text="Book Details:", font=("Arial", 18, "bold"))
        self.book_details_label.grid(
            row=3, column=0, columnspan=2, pady=10, sticky="n")

        self.book_details_text = ctk.CTkTextbox(
            self, wrap="word", font=("Arial", 14), height=150, width=400)
        self.book_details_text.grid(
            row=4, column=0, rowspan=2, columnspan=2, padx=10, pady=10, sticky="ns")
        self.book_details_text.configure(state="disabled")

        # Fine Receipt ID Entry (hidden initially)
        self.fine_receipt_label = ctk.CTkLabel(
            self, text="Enter Fine Receipt ID:", font=("Arial", 16))
        self.fine_receipt_entry = ctk.CTkEntry(
            self, placeholder_text="Enter Fine Receipt ID", width=300)

        # Return Book Button
        self.return_button = ctk.CTkButton(
            self, text="Return Book", command=self.return_book, fg_color="green")
        self.return_button.grid(row=7, column=0, columnspan=2, pady=20)

    def fetch_book_details(self):
        """Fetch and display book details based on the entered Book ID."""
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty!")
            return

        # Fetch book details
        book_details = self.master.admin.get_issued_book_details(book_id)
        if not book_details[0]:
            messagebox.showerror("Error", f"Book not found: {book_details[1]}")
            return

        book = book_details[1]

        issued_date = book['issue_date'].strftime("%d-%m-%Y")
        fine_result = self.master.admin.calculate_fine(book_id)
        self.return_user_id = book['user_id']

        # Display book details
        details = (
            f"Book ID: {book['book_id']}\n"
            f"Title: {book['title']}\n"
            f'username: {book["username"]}\n'
            f"Issued Date: {issued_date}\n"
            f"Fine: {'₹' + str(fine_result[1]) if fine_result[0] else 'No Fine'}"
        )
        self.book_details_text.configure(state="normal")
        self.book_details_text.delete("1.0", "end")
        self.book_details_text.insert("1.0", details)
        self.book_details_text.configure(state="disabled")

        # Show fine receipt entry if fine exists
        if fine_result[0]:
            self.fine_receipt_label.grid(
                row=6, column=0, padx=10, pady=10, sticky="e")
            self.fine_receipt_entry.grid(
                row=6, column=1, padx=10, pady=10, sticky="w")
        else:
            self.fine_receipt_label.grid_forget()
            self.fine_receipt_entry.grid_forget()

    def return_book(self):
        """Handle the book return process."""
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            messagebox.showerror("Error", "Book ID cannot be empty!")
            return

        # Check for fine receipt ID if fine exists
        fine_result = self.master.admin.calculate_fine(book_id)
        if fine_result[0]:
            fine_receipt_id = self.fine_receipt_entry.get().strip()
            if not fine_receipt_id:
                messagebox.showerror("Error", "Fine receipt ID is required!")
                return

        # Return the book
        result = self.master.admin.return_book(self.return_user_id, book_id)
        if result[0]:
            messagebox.showinfo("Success", "Book returned successfully!")
            self.book_id_entry.delete(0, "end")
            self.book_details_text.configure(state="normal")
            self.book_details_text.delete("1.0", "end")
            self.book_details_text.configure(state="disabled")
            self.fine_receipt_label.grid_forget()
            self.fine_receipt_entry.grid_forget()
        else:
            messagebox.showerror(
                "Error", f"Failed to return book: {result[1]}")


class add_student_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.master.admin.is_verified = is_verified
        self.master.admin.user_type = user_type
        self.user_id = userid

        self.label = ctk.CTkLabel(
            self, text="add_student_frame", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class admin_menu(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master, width=200, fg_color='#444444')
        self.app = app
        self.master = master
        self.admin = librarian()
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = user_id

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(tuple(range(0, 11)), weight=1, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Admin Menu", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")

        self.dashboard_button = ctk.CTkButton(
            self, text="Dashboard", command=self.master.show_admin_dashboard)
        self.dashboard_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="news")

        self.view_students_button = ctk.CTkButton(
            self, text="View students", command=self.master.view_students)
        self.view_students_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.add_book_button = ctk.CTkButton(
            self, text="Add Book", command=self.master.add_book_dashboard)
        self.add_book_button.grid(
            row=3, column=0, padx=10, pady=10, sticky="news")

        self.remove_book_button = ctk.CTkButton(
            self, text="Remove Book", command=self.master.remove_book_dashboard)
        self.remove_book_button.grid(
            row=4, column=0, padx=10, pady=10, sticky="news")

        self.issue_book_button = ctk.CTkButton(
            self, text="Issue Book", command=self.master.issue_book_dashboard)
        self.issue_book_button.grid(
            row=5, column=0, padx=10, pady=10, sticky="news")

        self.return_book_button = ctk.CTkButton(
            self, text="Return Book", command=self.master.return_book_dashboard)
        self.return_book_button.grid(
            row=6, column=0, padx=10, pady=10, sticky="news")

        self.add_student_button = ctk.CTkButton(
            self, text="Add user", command=self.master.add_student_dashboard)
        self.add_student_button.grid(
            row=7, column=0, padx=10, pady=10, sticky="news")

        self.logout_button = ctk.CTkButton(
            self, text="Logout", command=self.master.logout)
        self.logout_button.grid(
            row=8, column=0, padx=10, pady=10, sticky="news")


class admin_dashboard(ctk.CTkFrame):
    def __init__(self, master, app, user_id, username, is_verified, user_type):
        super().__init__(master, bg_color='#aeb6bf')
        self.app = app
        self.master = master
        self.admin = librarian()
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = user_id
        self.username = username

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(2, weight=3, uniform='a')
        self.grid_rowconfigure(3, weight=4, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Admin Dashboard", font=("Ubuntu Light", 16),)
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class student_panel(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        res = self.student.get_user_details(self.user_id)
        if res[0]:
            self.username = res[1]

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=9, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')

        self.menu = student_menu(
            self, app, user_id, is_verified, user_type)
        self.menu.grid(row=0, column=0, sticky="nsew")
        # self.menu.grid_rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self, text="Student Panel", font=("Arial", 20))
        self.label.grid(row=0, column=1, sticky="n")

        self.view_books_frame = student_view_books_frame(
            self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
        self.view_books_frame.grid(row=0, column=1, sticky="nsew")

        self.student_dashboard = student_dashboard(
            self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
        self.student_dashboard.grid(row=0, column=1, sticky="nsew")

    def view_books(self):
        self.view_books_frame.tkraise()

    def reserve_book(self):
        pass

    def show_student_dashboard(self):
        self.student_dashboard.tkraise()

    def reserve_book_dashboard(self):
        self.reserve_book_frame = reserve_book_frame(
            self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
        self.reserve_book_frame.grid(row=0, column=1, sticky="nsew")
        self.reserve_book_frame.tkraise()

    def reset_frame(self, master):
        for widget in master.winfo_children():
            widget.destroy()

    def create_search_frame(self, search_key=None):

        # Create a new search_book_frame
        self.search_frame = search_book_frame(
            self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type, search_key)
        self.search_frame.grid(row=0, column=1, sticky="nsew")
        self.search_frame.tkraise()

    def show_book_frame(self, book_res):
        # Create a new book_interface_frame
        self.book_interface_frame = book_interface_frame(
            self, self.app, self.user_id, book_res)
        self.book_interface_frame.grid(row=0, column=1, sticky="nsew")
        self.book_interface_frame.tkraise()

    def logout(self):
        self.student.is_verified = False
        self.student.user_type = None
        self.app.show_login()


class student_menu(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master, width=200, fg_color='#444444')
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(tuple(range(0, 11)), weight=1, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Student Menu", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")

        self.dashboard_button = ctk.CTkButton(
            self, text="Dashboard", command=self.master.show_student_dashboard)
        self.dashboard_button.grid(
            row=4, column=0, padx=10, pady=10, sticky="news")

        self.view_books_button = ctk.CTkButton(
            self, text="View Books", command=self.master.view_books)
        self.view_books_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="news")

        self.reserve_book_button = ctk.CTkButton(
            self, text="Reserve Book", command=self.master.reserve_book_dashboard)
        self.reserve_book_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.logout_button = ctk.CTkButton(
            self, text="Logout", command=self.master.logout)
        self.logout_button.grid(
            row=3, column=0, padx=10, pady=10, sticky="news")


class student_dashboard(ctk.CTkFrame):
    def __init__(self, master, app, user_id,  username, is_verified, user_type):
        super().__init__(master, bg_color='#aeb6bf')
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id
        self.username = username

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(1, weight=2, uniform='a')
        self.grid_rowconfigure(2, weight=3, uniform='a')
        self.grid_rowconfigure(3, weight=4, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="A book is a dream that you hold in your hands. ~Jack", font=("Ubuntu Light", 16),)
        self.label.grid(row=0, column=0, pady=20, sticky="n")

        self.label = ctk.CTkLabel(
            self, text=f"Hey, {self.username} Welcome Back..!", font=("Trebuchet MS", 22), )
        self.label.grid(row=1, column=0, padx=10, pady=20, sticky="w")

        self.search_bar = ctk.CTkEntry(
            self, placeholder_text="Search for books", width=400, height=50, )
        self.search_bar.grid(row=2, column=0, pady=10, sticky="n")

        self.search_button = ctk.CTkButton(
            self, text="Search", command=self.show_searhch_frame)
        self.search_button.grid(row=2, column=0, padx=5, )

        self.suggestions_label = ctk.CTkLabel(
            self, text="Suggestions", font=("Arial", 20))
        self.suggestions_label.grid(
            row=3, column=0, padx=10, pady=20, sticky="nw")

        self.book_suggestions = book_suggestion_frame(
            self, self.app, self.user_id, None, self.student.user_type)
        self.book_suggestions.grid(row=3, column=0, sticky='nesw')

    def show_searhch_frame(self):
        search_key = self.search_bar.get()
        self.master.create_search_frame(
            search_key=search_key,
        )


class book_suggestion_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master,  width=550, height=250)
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        self.grid_columnconfigure((0, 4), weight=1, uniform='a')
        self.grid_rowconfigure((0), weight=4, )
        self.grid_rowconfigure((1), weight=1, )
        self.img_pathes, self.img_id = self.cover_image_gen()
        for i in range(0, 6):
            try:
                self.image = Image.open(self.img_pathes[i])
                # self.image.show()
            except Exception as e:
                print(f"Error loading image: {e}")
            if self.image:
                my_image = ctk.CTkImage(light_image=self.image,
                                        dark_image=self.image, size=(150, 200))
                self.book_name = self.get_book_details(self.img_id[i])
                self.image_label = ctk.CTkButton(
                    self, image=my_image, text='', command=lambda book_name=self.book_name: self.openBook(book_name), fg_color='transparent')
                # self.image_label.pack()
                self.image_label.grid(
                    row=0, column=i, padx=10, pady=20, sticky="news")

                self.book_label = ctk.CTkLabel(
                    self, text=self.book_name, font=("Arial", 12))
                self.book_label.grid(
                    row=1, column=i, padx=5, pady=5, sticky="news")

    def get_book_details(self, image_id):
        book_details = self.student.get_book_details(
            key_name="image_id",
            key_value=image_id,
            columnName='title',
        )
        book_details = book_details[1]
        if book_details[0]:
            size = len(book_details)
            if size <= 25:
                return book_details
            else:
                book_details = book_details[:25]+'...'
                return book_details

    def cover_image_gen(self):
        img = []
        img_pathes = []
        while len(img) < 6:
            val = randint(1001, 1031)
            if val not in img:
                img.append(val)
                img_pathes.append(f"coverpages/{val}.png")
        return img_pathes, img

    def openBook(self, book_name):
        # Implement the logic to open the book
        print(f"Opening book: {book_name}")


class reserve_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, username, is_verified, user_type):
        super().__init__(master,)
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(tuple(range(0, 1)), weight=1, uniform='a')
        self.grid_rowconfigure((1), weight=6, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Reserve Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")

        self.style = ttk.Style(self)
        self.configure_style()
        self.table = ttk.Treeview(self, columns=(
            "Title", 'status', 'reserved'), show="headings", )
        self.table.heading("Title", text="Title")
        self.table.heading("status", text="status")
        self.table.heading("reserved", text="reserved")

        self.table.column("Title", width=150)
        self.table.column("status", width=100, anchor="center")
        self.table.column("reserved", width=100, anchor="center")

        self.update_table(self.table)
        self.table.grid(row=1, column=0, padx=50, pady=20, sticky="news")
        self.table.bind("<Double-1>", self.on_item_select)

    def on_item_select(self, event):

        region = self.table.identify_region(event.x, event.y)
        print(region)
        if region == "cell":
            column = self.table.identify_column(event.x)
            item = self.table.identify_row(event.y)
            item_values = self.table.item(item, "values")
            print(
                f"Selected item: {item}, Column: {column}, Values: {item_values}")

    def update_table(self, table):
        table_children = self.student.get_reserve_books(self.user_id)
        # print(table_children)
        if table_children[0]:

            table_children = table_children[1]
            # print(table_children)

            for i in range(len(table_children)):
                book_id = table_children[i]['book_id']
                title = self.student.get_book_details(
                    key_name="book_id",
                    key_value=book_id,
                    columnName='title',
                )[1]
                s_title = title[:40] + \
                    '...' if len(title) > 40 else title
                status = self.student.check_book_issued(book_id)[0]
                self.table.insert("", "end", values=(
                    s_title,
                    status,
                    'reserved'
                ))

    def configure_style(self):
        """Configures the dark theme for the Treeview"""
        self.style.theme_use("clam")  # Use 'clam' as the base theme

        # Treeview background, text color, and row height
        self.style.configure("Treeview",
                             background="#333333",
                             foreground="white",
                             rowheight=25,
                             fieldbackground="#333333")

        # Selected row color
        self.style.map("Treeview",
                       background=[("selected", "#555555")],
                       foreground=[("selected", "white")])

        # Heading styling
        self.style.configure("Treeview.Heading",
                             background="#444444",
                             foreground="white",
                             font=("Arial", 10, "bold"),
                             relief="solid",  # Adds border for heading
                             borderwidth=1,
                             )
        self.style.configure("Bordered.Treeview.Row",
                             relief="solid",  # Border for each row
                             borderwidth=1)


class search_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, username, is_verified, user_type, search_key):
        super().__init__(master)
        self.app = app
        self.master = master
        self.student = student()
        self.student.user_id = user_id
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        # Initialize search_key
        self.search_key = search_key.strip() if search_key else ""

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')

        self.style = ttk.Style(self)
        self.configure_style()
        self.table = ttk.Treeview(self, columns=(
            "Title", 'author'), show="headings")
        self.table.heading("Title", text="Title")
        self.table.heading("author", text="Author")

        self.table.column("Title", width=150)
        self.table.column("author", width=150)
        self.update_table(self.table)
        self.table.grid(row=0, column=0, padx=50, pady=20, sticky="nsew")

        self.table.bind("<Double-1>", self.on_item_select)

    def on_item_select(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            book_title = item['values'][0]
            book_author = item['values'][1]
            res = self.student.search_book(
                book_id=self.search_book_id, author=book_author)
            if res[0]:
                res = res[1][0]
                book_id = res['book_id']
                is_book_issued = self.student.check_book_issued(book_id)[0]

                book_res = {
                    "title": res['title'],
                    "author": res['author'],
                    "genre": res['genre'],
                    "isbn": res['isbn'],
                    "publisher": res['publisher'],
                    "published_year": res['published_year'],
                    "pages": res['pages'],
                }
                book_res['status'] = is_book_issued
                book_res['image_id'] = res['image_id']
                book_res['book_id'] = book_id
                print(book_res)
                self.master.show_book_frame(book_res)
                # print(res[1])

        else:
            return None, None

    def search_books(self):
        if not self.search_key:
            messagebox.showerror("Error", "Search field cannot be empty!")
            return None

        # Perform the search
        res = self.student.search_book_by_title(self.search_key)
        if res[0]:
            search_results = []
            for book in res[1]:
                title = book['title'][:40] + \
                    '...' if len(book['title']) > 40 else book['title']
                search_results.append(
                    {"title": title, "author": book['author'], 'book_id': book['book_id']})
                self.search_book_id = book['book_id']
            return search_results
        else:
            return None

    def update_table(self, table):
        search_results = self.search_books()
        if search_results:
            for book in search_results:
                table.insert("", "end", values=(book['title'], book['author']))
        else:
            table.insert("", "end", values=("No books found", ""))

    def configure_style(self):
        """Configures the dark theme for the Treeview"""
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="#333333",
                             foreground="white",
                             rowheight=25,
                             fieldbackground="#333333")

        self.style.map("Treeview",
                       background=[("selected", "#555555")],
                       foreground=[("selected", "white")])

        # Heading styling
        self.style.configure("Treeview.Heading",
                             background="#333333",
                             foreground="white",
                             font=("Arial", 10, "bold"),
                             relief="solid",
                             borderwidth=1,
                             )
        self.style.configure("Bordered.Treeview.Row",
                             relief="solid",
                             borderwidth=1)


class book_interface_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, book_res):
        super().__init__(master)
        self.app = app
        self.master = master
        self.user_id = user_id
        self.student = student()
        self.student.is_verified = True
        self.student.user_type = "student"
        self.student.user_id = user_id
        self.book_res = book_res

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(tuple(range(13)), weight=1, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Book Details", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="nesw")

        self.cover_image = Image.open(
            f"coverpages/{self.book_res['image_id']}.png")
        self.cover_image = ctk.CTkImage(light_image=self.cover_image,
                                        dark_image=self.cover_image, size=(250, 330))
        self.cover_image_label = ctk.CTkLabel(
            self, image=self.cover_image, text='')
        self.cover_image_label.grid(
            row=1, column=0, rowspan=10, padx=10, pady=5, sticky="news")
        self.title_label = ctk.CTkLabel(
            self, text=f"Title: {self.book_res['title']}", font=("Arial", 16))
        self.title_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.author_label = ctk.CTkLabel(
            self, text=f"Author: {self.book_res['author']}", font=("Arial", 16))
        self.author_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.publisher_label = ctk.CTkLabel(
            self, text=f"Publisher: {self.book_res['publisher']}", font=("Arial", 16))
        self.publisher_label.grid(
            row=4, column=1, padx=10, pady=5, sticky="w")
        self.published_year_label = ctk.CTkLabel(
            self, text=f"Published Year: {self.book_res['published_year']}", font=("Arial", 16))
        self.published_year_label.grid(
            row=5, column=1, padx=10, pady=5, sticky="w")

        self.pages_label = ctk.CTkLabel(
            self, text=f"Pages: {self.book_res['pages']}", font=("Arial", 16))
        self.pages_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.isbn_label = ctk.CTkLabel(
            self, text=f"ISBN: {self.book_res['isbn']}", font=("Arial", 16))
        self.isbn_label.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.genre_label = ctk.CTkLabel(
            self, text=f"Genre: {self.book_res['genre']}", font=("Arial", 16))
        self.genre_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.status_label = ctk.CTkLabel(
            self, text=f"Status: {self.book_res['status']}", font=("Arial", 16))
        self.status_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.reserve_button = ctk.CTkButton(
            self, text="Reserve Book", command=self.reserve_book, fg_color='green')
        self.reserve_button.grid(
            row=10, column=1, padx=30, pady=5, sticky="news")

    def reserve_book(self):
        self.student.reserve_book(self.user_id, self.book_res['book_id'])
        messagebox.showinfo("Success", "Book reserved successfully!")


class student_view_books_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, username, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')
        self.grid_rowconfigure(1, weight=5, uniform='a')
        self.label = ctk.CTkLabel(
            self, text="View Books", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")
        self.style = ttk.Style(self)
        self.configure_style()
        self.table = ttk.Treeview(self, columns=(
            "Title", 'issue_date', 'return_date', 'Penalty'), show="headings", )
        self.table.heading("Title", text="Title")
        self.table.heading("issue_date", text="issued")
        self.table.heading("return_date", text="returned")
        self.table.heading("Penalty", text="Penalty")

        self.table.column("Title", width=150)
        self.table.column("issue_date", width=100, anchor="center")
        self.table.column("return_date", width=100, anchor="center")
        self.table.column("Penalty", width=80, anchor="center")
        self.update_table(self.table)
        self.table.grid(row=1, column=0, padx=50, pady=20, sticky="ew")

        res = self.student.view_shelf(
            user_id=self.user_id,
        )

    def configure_style(self):
        """Configures the dark theme for the Treeview"""
        self.style.theme_use("clam")  # Use 'clam' as the base theme

        # Treeview background, text color, and row height
        self.style.configure("Treeview",
                             background="#333333",
                             foreground="white",
                             rowheight=25,
                             fieldbackground="#333333")

        # Selected row color
        self.style.map("Treeview",
                       background=[("selected", "#555555")],
                       foreground=[("selected", "white")])

        # Heading styling
        self.style.configure("Treeview.Heading",
                             background="#444444",
                             foreground="white",
                             font=("Arial", 10, "bold"),
                             relief="solid",  # Adds border for heading
                             borderwidth=1,
                             )
        self.style.configure("Bordered.Treeview.Row",
                             relief="solid",  # Border for each row
                             borderwidth=1)

    def update_table(self, table):
        table_children = self.student.issued_books_table(
            user_id=self.user_id
        )
        if table_children[0]:
            for i in range(table_children[1]):
                self.table.insert("", "end", values=(
                    table_children[2][i]['title'],
                    table_children[2][i]['issue_date'],
                    table_children[2][i]['return_date'],
                    # table_children[2][i]['penalty']
                    0
                ))
        else:
            self.table.insert("", "end", values=(
                ' ',
                'No books issued',
                ' ',
                ' ',
                0
            ))
            return


if __name__ == "__main__":
    app = LibraryManagement()

    app.mainloop()
