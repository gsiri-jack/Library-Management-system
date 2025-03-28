import customtkinter as ctk


class LibraryManagement(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management system")
        self.geometry("600x400")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login()

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
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            # simple authentication
            self.show_dashboard()
        else:
            error_label = ctk.CTkLabel(
                self.container, text="Invalid Credentials!", text_color="red")
            error_label.pack()

    def show_dashboard(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.container)
        frame.pack(expand=True)

        label = ctk.CTkLabel(
            frame, text="Welcome to the Library", font=("Arial", 20))
        label.pack(pady=20)

        logout_button = ctk.CTkButton(
            frame, text="Logout", command=self.show_login)
        logout_button.pack(pady=10)


if __name__ == "__main__":
    app = LibraryManagement()
    app.mainloop()
