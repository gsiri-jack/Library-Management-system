import customtkinter as ctkinter


class loginPage(ctkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#CD5C5C")
        self.label = ctkinter.CTkLabel(self, text="login pge").pack()


class Application(ctkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sample")
        self.geometry("600x600")
        self.button = ctkinter.CTkButton(
            self, command=self.button_click, fg_color="#870b0b", hover_color="#9c3636").pack()
        self.loginP = loginPage(self).pack()
        self.mainloop()

    def button_click(self):
        self.label = ctkinter.CTkLabel(self, text="hello world").pack()


Application()
