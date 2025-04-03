import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from databaseQuery import librarian, student, services
from PIL import Image
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

        self.user_id = "b"
        self.password = 'b'

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

        self.label = ctk.CTkLabel(self, text="Admin Panel", font=("Arial", 20))
        self.label.pack(pady=20)

        self.create_user_button = ctk.CTkButton(
            self, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=10)

        self.logout_button = ctk.CTkButton(
            self, text="Logout", command=self.logout)
        self.logout_button.place(x=5, y=20)

    def create_user(self):
        # Example functionality for creating a user
        self.admin.create_user(
            user_id="b",
            username="alice",
            password="b",
            user_type="student"
        )
        messagebox.showinfo("Success", "User created successfully!")

    def logout(self):
        self.admin.is_verified = False
        self.admin.user_type = None
        self.app.show_login()


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
        self.grid_columnconfigure(1, weight=3, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')

        self.menu = student_menu(
            self, app, user_id, is_verified, user_type)
        self.menu.grid(row=0, column=0, sticky="nsew")
        # self.menu.grid_rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self, text="Student Panel", font=("Arial", 20))
        self.label.grid(row=0, column=1, sticky="n")

        self.reserve_book_frame = reserve_book_frame(
            self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
        self.reserve_book_frame.grid(row=0, column=1, sticky="nsew")

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
        self.reserve_book_frame.tkraise()

    def reset_frame(self, master):
        for widget in master.winfo_children():
            widget.destroy()

    def logout(self):
        self.student.is_verified = False
        self.student.user_type = None
        self.app.show_login()


class student_menu(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master, width=250, fg_color='#444444')
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

        # Example button to demonstrate functionality
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

        self.dashboard_button = ctk.CTkButton(
            self, text="Dashboard", command=self.master.show_student_dashboard)
        self.dashboard_button.grid(
            row=4, column=0, padx=10, pady=10, sticky="news")


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
            self, text="Search", command=self.search_books)
        self.search_button.grid(row=2, column=0, padx=5, )

        self.suggestions_label = ctk.CTkLabel(
            self, text="Suggestions", font=("Arial", 20))
        self.suggestions_label.grid(
            row=3, column=0, padx=10, pady=20, sticky="nw")

        self.book_suggestions = book_suggestion_frame(
            self, self.app, self.user_id, None, self.student.user_type)
        self.book_suggestions.grid(row=3, column=0, sticky='sw')

    def search_books(self):
        pass


class book_suggestion_frame(ctk.CTkFrame):
    def __init__(self, master, app, user_id, is_verified, user_type):
        super().__init__(master,  width=500, height=250)
        self.app = app
        self.master = master
        self.student = student()
        self.student.is_verified = is_verified
        self.student.user_type = user_type
        self.user_id = user_id

        self.grid_columnconfigure((0, 1), weight=1, uniform='a')
        self.grid_rowconfigure((0), weight=4, )
        self.grid_rowconfigure((1), weight=1, )

        try:
            self.image = Image.open("steve.jpg")
            # self.image.show()
        except Exception as e:
            print(f"Error loading image: {e}")

        my_image = ctk.CTkImage(light_image=self.image,
                                dark_image=self.image, size=(200, 150))

        self.image_label = ctk.CTkLabel(self, image=my_image, text='')
        # self.image_label.pack()
        self.image_label.grid(row=0, column=0, pady=20, sticky="news")

        my_image2 = ctk.CTkImage(light_image=self.image,
                                 dark_image=self.image, size=(200, 150))

        self.image_label2 = ctk.CTkLabel(self, image=my_image2, text='')
        # self.image_label.pack()
        self.image_label2.grid(row=0, column=1, padx=10,
                               pady=10, sticky="news")

        self.book_name = ctk.CTkLabel(self,  text='Steve', font=("Trebuchet MS", 22))
        self.book_name.grid(row=1, column=0, sticky='n')


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
        self.grid_rowconfigure(tuple(range(0, 2)), weight=1, uniform='a')

        self.label = ctk.CTkLabel(
            self, text="Reserve Book", font=("Arial", 20))
        self.label.grid(row=0, column=0, pady=20, sticky="n")


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
            messagebox.showerror("Error", "No books found!")
            return


if __name__ == "__main__":
    app = LibraryManagement()

    app.mainloop()
