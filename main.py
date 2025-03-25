import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class App(tk.Tk):
  def __init__(self):
    super().__init__()

    # configure the root window
    self.title('My Awesome App')s
    self.geometry('600x600+50+50')

    # label
    self.label = ttk.Label(self, text='Hello, Tkinter!')
    self.label.pack()

    # button
    self.button = ttk.Button(self, text='Click Me',command=self.button_clicked)
    # self.button['command'] = self.button_clicked
    self.button.pack()

  def button_clicked(self):
    self.label = ttk.Label(self, text='add, Tkinter!')
    self.label.pack()
    

if __name__ == "__main__":
  app = App()
  app.mainloop()