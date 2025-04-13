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
            self, self.app, self.user_id, is_verified=True, user_type="admin")
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
        pass

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
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
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
            self, text="Search", command=self.reset_view_studetnts_frame)
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

    def update_table(self, table):
        pass


class add_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = userid

        self.label = ctk.CTkLabel(
            self, text="Add Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class remove_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = userid

        self.label = ctk.CTkLabel(
            self, text="remove Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class issue_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = userid

        self.label = ctk.CTkLabel(
            self, text="issue Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class return_book_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
        self.user_id = userid

        self.label = ctk.CTkLabel(
            self, text="return Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


class add_student_frame(ctk.CTkFrame):
    def __init__(self, master, app, userid, is_verified, user_type):
        super().__init__(master)
        self.app = app
        self.master = master
        self.userid = userid
        self.admin.is_verified = is_verified
        self.admin.user_type = user_type
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
            row=4, column=0, padx=10, pady=10, sticky="news")

        self.view_students_button = ctk.CTkButton(
            self, text="View students", command=self.master.view_students)
        self.view_students_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="news")

        self.add_book_button = ctk.CTkButton(
            self, text="Add Book", command=self.master.add_book_dashboard)
        self.add_book_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.remove_book_button = ctk.CTkButton(
            self, text="Remove Book", command=self.master.remove_book_dashboard)
        self.remove_book_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.issue_book_button = ctk.CTkButton(
            self, text="Issue Book", command=self.master.issue_book_dashboard)
        self.issue_book_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.return_book_button = ctk.CTkButton(
            self, text="Return Book", command=self.master.return_book_dashboard)
        self.return_book_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.add_student_button = ctk.CTkButton(
            self, text="Add user", command=self.master.add_student_dashboard)
        self.add_student_button.grid(
            row=2, column=0, padx=10, pady=10, sticky="news")

        self.logout_button = ctk.CTkButton(
            self, text="Logout", command=self.master.logout)
        self.logout_button.grid(
            row=3, column=0, padx=10, pady=10, sticky="news")


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
