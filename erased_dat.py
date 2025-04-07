# # 0304-18:48
# self.grid_columnconfigure(0, weight=1, uniform='a')
#         self.grid_columnconfigure(1, weight=10, uniform='a')
#         self.grid_rowconfigure(0, weight=1, uniform='a')

#         self.menu = student_menu(
#             self, app, user_id, is_verified, user_type)
#         self.menu.grid(row=0, column=0, sticky="nsew")
#         # self.menu.grid_rowconfigure(0, weight=1)

#         self.label = ctk.CTkLabel(
#             self, text="Student Panel", font=("Arial", 20))
#         self.label.grid(row=0, column=1, sticky="n")

#         self.reserve_book_frame = reserve_book_frame(
#             self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
#         self.reserve_book_frame.grid(row=0, column=1, sticky="nsew")

#         self.view_books_frame = student_view_books_frame(
#             self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
#         self.view_books_frame.grid(row=0, column=1, sticky="nsew")

#         self.student_dashboard = student_dashboard(
#             self, self.app, self.user_id, self.username, self.student.is_verified, self.student.user_type)
#         self.student_dashboard.grid(row=0, column=1, sticky="nsew")