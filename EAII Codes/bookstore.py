import csv
import tabulate
import os
user = int(input("Bookstore Management System:"
                 "\n1. Add Book"
                 "  2. View Books"
                 "\n3. Search Book"
                 "  4. Update Book"
                 "\n5. Delete Book"
                 "  6. Exit"
                 "\nEnter your choice: "))
def book_check(ID):
    file = open("books.csv", "r")
    reader = csv.reader(file)
    all_rows = list(reader)
    file.close()
    for row in all_rows[1:]:
        if ID == row[0]:
            return True
    return False
if user == 1:
    book_id = input("Enter book ID: ")
    if book_check(book_id):
        print("This ID already exists in the library.")
        exit()
    title = input("Enter book title: ")
    author_name = input("Enter book author's name: ")
    price = input("Enter book price: ")
    if (
        book_id.isalnum() and
        title.isalpha() and
        author_name.isalpha() and
        price.isnumeric()
    ):
        def log_to_csv():
            file_exists = os.path.exists("books.csv")
            books_file = open("books.csv", "a", newline="")
            writer = csv.writer(books_file)
            if not file_exists:
                writer.writerow(["ID", "Title", "Author Name", "Price"])
            writer.writerow([book_id, title, author_name, price])
            books_file.close()
        log_to_csv()
        print("Book added successfully!")
    else:
        print("Invalid input! One or more inputs are invalid.")
        exit()
elif user == 2:
    file = open("books.csv","r")
    reader = csv.reader(file)
    all_rows = list(reader)
    file.close()
    if len(all_rows) > 1:
        headers = all_rows[0]
        book_data = all_rows[1:]
        print(tabulate.tabulate(book_data, headers=headers, tablefmt="grid"))
    else:
        print("There is no book stored in the library.")
elif user == 3:
    file = open("books.csv","r")
    reader = csv.reader(file)
    all_rows = list(reader)
    ID = input("Enter book ID: ")
    for row in all_rows:
        if row[0] == ID:
            headers = all_rows[0]
            book_data = row[1:]
            print(tabulate.tabulate(book_data, headers=headers, tablefmt="grid"))
        else:
            print("Book ID not found.")
elif user == 4:
    book_id = input("Enter book ID: ")

    if not book_check(book_id):
        print("Book ID not found.")
    else:
        file = open("books.csv", "r", newline="", encoding="utf-8")
        reader = csv.reader(file)
        all_rows = list(reader)
        file.close()

        updated = False
        for row in all_rows:
            if row and row[0] == book_id:
                new_title = input("Enter new book title: ")
                new_author = input("Enter new book author name: ")
                new_price = input("Enter new book price: ")

                if (
                        book_id.isalnum() and
                        new_title.isalpha() and
                        new_author.isalpha() and
                        new_price.isnumeric()
                ):
                    row[1] = new_title
                    row[2] = new_author
                    row[3] = new_price
                    updated = True
                    print("The book's details were successfully updated.")
                else:
                    print("Invalid input! One or more inputs are invalid.")
                break

        if updated:
            file = open("books.csv", "w", newline="")
            writer = csv.writer(file)
            writer.writerows(all_rows)
            file.close()


elif user==5:
    file = open("books.csv","r")
    reader = csv.reader(file)
    all_rows = list(reader)
    ID = input("Enter book ID: ")
    for row in all_rows:
        if row == ID:
            all_rows.remove(row)
            print("Book deleted successfully.")
    else:
        print("The book does not exist in the library.")
elif user == 6:
    print("Successfully exited the program!")
    exit()