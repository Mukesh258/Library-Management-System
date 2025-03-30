import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Create custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)
        
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Mukesh@2303",
                database="LibraryDB",
                auth_plugin='mysql_native_password',
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            self.cursor = self.db.cursor(buffered=True)
            messagebox.showinfo("Success", "Connected to database!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database connection failed: {err}")
            root.destroy()
            return

        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0', pady=20)
        main_frame.pack(expand=True)

        # Title Label
        tk.Label(main_frame, text="Library Management System", 
                font=self.title_font, bg='#f0f0f0', fg='#333333').pack(pady=20)

        # Create buttons with improved styling
        buttons = [
            ("Add Book", self.add_book_window),
            ("Issue Book", self.issue_book_window),
            ("Return Book", self.return_book_window),
            ("List Books", self.list_books),
            ("Exit", root.quit)
        ]

        for text, command in buttons:
            btn = tk.Button(main_frame, text=text, command=command,
                          font=self.button_font,
                          width=20,
                          bg='#4a90e2',
                          fg='white',
                          activebackground='#357abd',
                          activeforeground='white',
                          relief=tk.RAISED,
                          pady=5)
            btn.pack(pady=8)

    def create_entry_field(self, window, label_text):
        frame = tk.Frame(window, bg='#f0f0f0')
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, font=self.button_font, bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, font=("Helvetica", 10))
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def add_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")
        window.geometry("400x350")
        window.configure(bg='#f0f0f0')
        
        tk.Label(window, text="Add New Book", font=self.title_font, bg='#f0f0f0').pack(pady=15)
        
        title_entry = self.create_entry_field(window, "Title:")
        author_entry = self.create_entry_field(window, "Author:")
        publisher_entry = self.create_entry_field(window, "Publisher:")
        year_entry = self.create_entry_field(window, "Year:")

        def submit():
            if not all([title_entry.get(), author_entry.get(), publisher_entry.get(), year_entry.get()]):
                messagebox.showwarning("Warning", "All fields are required!")
                return
            try:
                query = "INSERT INTO Books (title, author, publisher, year, status) VALUES (%s, %s, %s, %s, 'Available')"
                self.cursor.execute(query, (
                    title_entry.get(),
                    author_entry.get(),
                    publisher_entry.get(),
                    year_entry.get()
                ))
                self.db.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")

        tk.Button(window, text="Submit", command=submit,
                 font=self.button_font, bg='#4a90e2', fg='white',
                 width=15).pack(pady=20)

    def issue_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Issue Book")
        window.geometry("600x500")
        window.configure(bg='#f0f0f0')

        tk.Label(window, text="Issue Book", font=self.title_font, bg='#f0f0f0').pack(pady=15)

        # Available books frame
        books_frame = tk.Frame(window, bg='#f0f0f0')
        books_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(books_frame, text="Available Books:", font=self.button_font, bg='#f0f0f0').pack()

        # Create Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(books_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(books_frame, columns=("ID", "Title", "Author"), 
                           show="headings", height=8, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading("ID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        
        tree.column("ID", width=80)
        tree.column("Title", width=250)
        tree.column("Author", width=200)
        tree.pack(pady=5, fill=tk.BOTH, expand=True)

        # Input fields frame
        input_frame = tk.Frame(window, bg='#f0f0f0')
        input_frame.pack(pady=10)

        book_id_entry = self.create_entry_field(input_frame, "Book ID:")
        student_id_entry = self.create_entry_field(input_frame, "Student ID:")

        # Student ID format help
        help_frame = tk.Frame(window, bg='#f0f0f0')
        help_frame.pack()
        tk.Label(help_frame, 
                text="Student ID Format: AP23110010175", 
                font=("Helvetica", 10, "bold"), 
                bg='#f0f0f0').pack()
        tk.Label(help_frame, 
                text="AP: State | 23: Year | 11: College | 001: Branch | 0175: Roll No", 
                font=("Helvetica", 9), 
                bg='#f0f0f0', 
                fg='#666666').pack()

        def validate_student_id(student_id):
            if len(student_id) != 13:
                return False, "Student ID must be 13 characters"
            if not student_id.startswith('AP'):
                return False, "Student ID must start with 'AP'"
            try:
                year = int(student_id[2:4])
                college = student_id[4:6]
                branch = int(student_id[6:9])
                roll = int(student_id[9:])
                if not (20 <= year <= 23):
                    return False, "Invalid year"
                if college != "11":
                    return False, "Invalid college code"
                if not (1 <= branch <= 999):
                    return False, "Invalid branch code"
                if not (1 <= roll <= 9999):
                    return False, "Invalid roll number"
                return True, ""
            except ValueError:
                return False, "Invalid format"

        def submit():
            if not all([book_id_entry.get(), student_id_entry.get()]):
                messagebox.showwarning("Warning", "All fields are required!")
                return

            student_id = student_id_entry.get().upper().strip()
            is_valid, error_msg = validate_student_id(student_id)
            if not is_valid:
                messagebox.showwarning("Invalid Student ID", error_msg)
                return

            try:
                # Convert book_id to integer for validation
                try:
                    book_id = int(book_id_entry.get())
                except ValueError:
                    messagebox.showwarning("Error", "Book ID must be a number!")
                    return

                # Verify if the book exists and is available
                self.cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
                book = self.cursor.fetchone()
                
                if not book:
                    messagebox.showwarning("Error", "Book does not exist!")
                    return
                    
                if book[5] != 'Available':
                    messagebox.showwarning("Error", "Book is not available!")
                    return

                # Check if student already has any books
                self.cursor.execute("""
                    SELECT COUNT(*) FROM Issued_Books 
                    WHERE student_id = %s
                """, (student_id,))
                book_count = self.cursor.fetchone()[0]
                
                if book_count >= 3:
                    messagebox.showwarning("Error", "Student has reached maximum book limit (3)!")
                    return

                # Issue the book
                issue_date = datetime.today().strftime('%Y-%m-%d')
                
                # Use parameterized query with explicit type conversion
                self.cursor.execute(
                    """INSERT INTO Issued_Books 
                       (book_id, student_id, issue_date) 
                       VALUES (%s, %s, %s)""",
                    (int(book_id), str(student_id), issue_date)
                )
                
                # Update book status
                self.cursor.execute(
                    "UPDATE Books SET status = 'Issued' WHERE book_id = %s",
                    (book_id,)
                )
                
                self.db.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                
                # Refresh the book list
                for item in tree.get_children():
                    tree.delete(item)
                self.cursor.execute("""
                    SELECT book_id, title, author 
                    FROM Books 
                    WHERE status='Available'
                    ORDER BY book_id
                """)
                for book in self.cursor.fetchall():
                    tree.insert("", "end", values=book)
                    
            except mysql.connector.Error as e:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to issue book: {e}")
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Populate available books
        self.cursor.execute("""
            SELECT book_id, title, author 
            FROM Books 
            WHERE status='Available'
            ORDER BY book_id
        """)
        for book in self.cursor.fetchall():
            tree.insert("", "end", values=book)

        # Buttons frame
        button_frame = tk.Frame(window, bg='#f0f0f0')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Issue Book", command=submit,
                 font=self.button_font, bg='#4a90e2', fg='white',
                 width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Clear", 
                 command=lambda: [book_id_entry.delete(0, tk.END), 
                                student_id_entry.delete(0, tk.END)],
                 font=self.button_font, bg='#4a90e2', fg='white',
                 width=15).pack(side=tk.LEFT, padx=5)

    def return_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Return Book")
        window.geometry("500x400")
        window.configure(bg='#f0f0f0')

        tk.Label(window, text="Return Book", font=self.title_font, bg='#f0f0f0').pack(pady=15)

        # Create frame for issued books
        books_frame = tk.Frame(window, bg='#f0f0f0')
        books_frame.pack(pady=10)

        tk.Label(books_frame, text="Currently Issued Books:", font=self.button_font, bg='#f0f0f0').pack()

        # Create Treeview for issued books
        tree = ttk.Treeview(books_frame, columns=("ID", "Title", "Student"), show="headings", height=5)
        tree.heading("ID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("Student", text="Student ID")
        tree.pack(pady=5)

        # Populate issued books
        self.cursor.execute("""
            SELECT b.book_id, b.title, i.student_id 
            FROM Books b 
            JOIN Issued_Books i ON b.book_id = i.book_id 
            WHERE b.status='Issued'
        """)
        for book in self.cursor.fetchall():
            tree.insert("", "end", values=book)

        book_id_entry = self.create_entry_field(window, "Book ID:")

        def submit():
            if not book_id_entry.get():
                messagebox.showwarning("Warning", "Book ID is required!")
                return
            try:
                book_id = book_id_entry.get()
                
                # Verify book exists and is issued
                self.cursor.execute("SELECT status FROM Books WHERE book_id = %s", (book_id,))
                result = self.cursor.fetchone()
                
                if result and result[0] == 'Issued':
                    self.cursor.execute("DELETE FROM Issued_Books WHERE book_id = %s", (book_id,))
                    self.cursor.execute("UPDATE Books SET status = 'Available' WHERE book_id = %s", (book_id,))
                    self.db.commit()
                    messagebox.showinfo("Success", "Book returned successfully!")
                    window.destroy()
                else:
                    messagebox.showwarning("Warning", "Book is not issued or doesn't exist!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {e}")

        tk.Button(window, text="Return Book", command=submit,
                 font=self.button_font, bg='#4a90e2', fg='white',
                 width=15).pack(pady=20)

    def list_books(self):
        window = tk.Toplevel(self.root)
        window.title("Book List")
        window.geometry("800x500")
        window.configure(bg='#f0f0f0')

        tk.Label(window, text="Library Book Inventory", 
                font=self.title_font, bg='#f0f0f0').pack(pady=15)

        # Create frame for books table
        books_frame = tk.Frame(window, bg='#f0f0f0')
        books_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Create Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(books_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(books_frame, columns=("ID", "Title", "Author", "Publisher", "Year", "Status"), 
                            show="headings", height=15, yscrollcommand=tree_scroll.set)
        
        # Configure scrollbar
        tree_scroll.config(command=tree.yview)

        # Define column widths and headings
        tree.column("ID", width=50)
        tree.column("Title", width=200)
        tree.column("Author", width=150)
        tree.column("Publisher", width=150)
        tree.column("Year", width=80)
        tree.column("Status", width=100)

        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Publisher", text="Publisher")
        tree.heading("Year", text="Year")
        tree.heading("Status", text="Status")

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate books
        try:
            self.cursor.execute("SELECT * FROM Books ORDER BY book_id")
            for book in self.cursor.fetchall():
                tree.insert("", "end", values=book)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch books: {e}")

        # Add refresh button
        def refresh_list():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            # Repopulate
            try:
                self.cursor.execute("SELECT * FROM Books ORDER BY book_id")
                for book in self.cursor.fetchall():
                    tree.insert("", "end", values=book)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh books: {e}")

        tk.Button(window, text="Refresh", command=refresh_list,
                 font=self.button_font, bg='#4a90e2', fg='white',
                 width=15).pack(pady=10)

    def validate_student_id(self, student_id):
        if len(student_id) != 13:
            return False, "Student ID must be 13 characters long"
        
        try:
            state = student_id[:2]
            year = int(student_id[2:4])
            college = student_id[4:6]
            branch = student_id[6:9]
            roll = int(student_id[9:])
            
            # Validation rules
            if state != "AP":
                return False, "State code must be 'AP'"
            if not (20 <= year <= 23):
                return False, "Year should be between 20-23"
            if college != "11":
                return False, "Invalid college code"
            if not (1 <= int(branch) <= 999):
                return False, "Branch code should be between 001-999"
            if not (1 <= roll <= 9999):
                return False, "Roll number should be between 0001-9999"
                
            return True, "Valid student ID"
        except ValueError:
            return False, "Invalid format"

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()