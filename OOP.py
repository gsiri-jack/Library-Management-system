# library management system
# view available books
# take a book rent if available
# submit the book
# add to queue
# add new books
class J_book:
    def __init__(self):
        self.bookSelf = {"001": "Atomic Habits", "002": "Rich Dad", "003": "The fall"}
        self.issuedShelf = []

    def displayBook(self):
        print("\n", "-"*20)
        for val in self.bookSelf:
            print(f"-{val}\t{self.bookSelf[val]}")
        print("", "-"*20, "\n")

    def addBook(self, bookid, bookname):
        if bookid in self.bookSelf.keys() or bookname in self.bookSelf.values():
            print("\nThat book already Exists .. Try another\n")
        else:
            self.bookSelf[bookid] = bookname
            print(f"\n{bookname} added successfully")
            print("-" * 15, "\n")

    def issueBook(self, bookid):
        if bookid not in self.bookSelf.keys():
            print("\nBook not found \n")
            return None
        if self.bookSelf[bookid] in self.issuedShelf:
            print("\nAlready issued\n")
        else:
            self.issuedShelf.append(self.bookSelf[bookid])
            print("\nBook Issued successfully \n")
            print("\nIssued Books: ")
            print(self.issuedShelf)
            print("-"*15, "\n")

    def submitBook(self, bookid):
        if bookid not in self.bookSelf.keys():
            print("\nBook not found \n")
            return None
        if self.bookSelf[bookid] in self.issuedShelf:
            self.issuedShelf.remove(self.bookSelf[bookid])
            print("\nBook submit Successfully\n")
        else:
            print("\nFirst issue the book\n")


obj = J_book()


while True:
    option = True
    print("+", "-" * 20, "+")
    print("|", "\t1 .View Shelf".ljust(20, " "), "|")
    print("|", "\t2 .Issue a Book".ljust(20, " "), "|")
    print("|", "\t3 .Submit a book".ljust(20, " "), "|")
    print("|", "\t4 .Add to Book".ljust(20, " "), "|")
    print("|", "\t0 .Quit".ljust(20, " "), "|")
    print("+", "-" * 20, "+")
    print()
    key = int(input("Select Your service: "))
    if key == 1:
        obj.displayBook()
    elif key == 2:
        bookId = (input("Enter BookId You want issue : "))
        obj.issueBook(bookId)
    elif key == 3:
        book_id = input("Enter BookID you want to submit : ")
        obj.submitBook(book_id)
    elif key == 4:
        bookId, bookName = input("Enter BookId and BookId Names >> Separated by  ',' : ").split(",")
        obj.addBook(bookId, bookName)
    elif key == 0:
        exit()
    else:
        print("\nThis feature is Enables soon --Try Again!!\n")
