import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import matplotlib.pyplot as plt
import qrcode
from PIL import Image, ImageTk
import os

# Predefined list of books
books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "price": 500},
    {"title": "1984", "author": "George Orwell", "price": 600},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 700},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 800},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "price": 900},
    {"title": "War and Peace", "author": "Leo Tolstoy", "price": 1200},
    {"title": "Ulysses", "author": "James Joyce", "price": 1500},
    {"title": "The Odyssey", "author": "Homer", "price": 1000},
    {"title": "Moby Dick", "author": "Herman Melville", "price": 1100},
    {"title": "Hamlet", "author": "William Shakespeare", "price": 950},
]

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Management System")
        self.username = ""
        self.selected_books = []
        self.is_dark_mode = False

        self.login_screen()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme()

    def update_theme(self):
        if self.is_dark_mode:
            self.root.configure(bg="black")
            for widget in self.root.winfo_children():
                widget.configure(bg="black", fg="white")
        else:
            self.root.configure(bg="pink")
            for widget in self.root.winfo_children():
                widget.configure(bg="pink", fg="black")

    def login_screen(self):
        self.clear_screen()
        self.update_theme()

        tk.Label(self.root, text="Welcome to the Library! 👋", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text="Please enter your name to continue:", font=("Helvetica", 12)).pack(pady=5)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        tk.Button(self.root, text="Login 🚪", command=self.login, font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, font=("Helvetica", 12)).pack(pady=5)

        # Language selection
        self.language_var = tk.StringVar(value="English")
        language_menu = ttk.Combobox(self.root, textvariable=self.language_var, values=["English", "Spanish", "French"])
        language_menu.pack(pady=5)
        language_menu.bind("<<ComboboxSelected>>", self.change_language)

    def change_language(self, event):
        selected_language = self.language_var.get()
        # Implement language change logic here (for simplicity, not implemented in this example)

    def login(self):
        name = self.name_entry.get().strip()
        if name:
            self.username = name
            self.book_selection_screen()
        else:
            messagebox.showerror("Input Error", "Name cannot be empty.")

    def book_selection_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.username}! 📖", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text="Select books to borrow:", font=("Helvetica", 12)).pack(pady=5)

        self.book_vars = []
        for book in books:
            var = tk.IntVar()
            cb = tk.Checkbutton(self.root, text=f"{book['title']} by {book['author']} - ₹{book['price']}", variable=var, font=("Helvetica", 10))
            cb.pack(anchor='w')
            self.book_vars.append((var, book))

        tk.Button(self.root, text="Proceed to Checkout 🛒", command=self.checkout_screen, font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.root, text="Feedback 💬", command=self.feedback_screen, font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self.root, text="Show Stats 📊", command=self.show_stats, font=("Helvetica", 12)).pack(pady=5)

    def checkout_screen(self):
        self.selected_books = [book for var, book in self.book_vars if var.get() == 1]
        if not self.selected_books:
            messagebox.showwarning("No Selection", "Please select at least one book.")
            return

        self.clear_screen()
        tk.Label(self.root, text="Checkout Summary 🧾", font=("Helvetica", 16)).pack(pady=10)

        total_price = sum(book['price'] for book in self.selected_books)
        discount = 0
        if total_price > 2000:
            discount = 50
            total_price -= discount

        for book in self.selected_books:
            tk.Label(self.root, text=f"{book['title']} by {book['author']} - ₹{book['price']}", font=("Helvetica", 10)).pack(anchor='w')

        tk.Label(self.root, text=f"Discount Applied: ₹{discount}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Total Price: ₹{total_price}", font=("Helvetica", 12, "bold")).pack(pady=5)

        tk.Button(self.root, text="Confirm and Borrow ✅", command=self.generate_qr_code, font=("Helvetica", 12)).pack(pady=10)

    def generate_qr_code(self):
        qr_data = f"Books borrowed by {self.username}: " + ", ".join(book['title'] for book in self.selected_books)
        qr = qrcode.make(qr_data)
        qr_path = "qr_code.png"
        qr.save(qr_path)

        self.clear_screen()
        tk.Label(self.root, text="Thank You! 🎉", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text=f"{self.username}, you have successfully borrowed the books.", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text="Your QR Code for Check-in/Check-out:", font=("Helvetica", 12)).pack(pady=5)

        img = Image.open(qr_path)
        img = img.resize((200, 200), Image.ANTIALIAS)
        self.qr_image = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.qr_image).pack(pady=10)

        tk.Button(self.root, text="Back to Home", command=self.book_selection_screen, font=("Helvetica", 12)).pack(pady=10)

    def feedback_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Member Feedback 💬", font=("Helvetica", 16)).pack(pady=10)

        feedback = simpledialog.askstring("Feedback", "Please provide your feedback:")
        if feedback:
            messagebox.showinfo("Feedback Received", "Thank you for your feedback!")
        else:
            messagebox.showwarning("No Feedback", "Feedback cannot be empty.")

        tk.Button(self.root, text="Back to Home", command=self.book_selection_screen, font=("Helvetica", 12)).pack(pady=10)

    def show_stats(self):
        self.clear_screen()
        tk.Label(self.root, text="Library Statistics 📊", font=("Helvetica", 16)).pack(pady=10)

        # Example data for chart
        book_titles = [book['title'] for book in books]
        book_prices = [book['price'] for book in books]

        plt.bar(book_titles, book_prices, color='pink')
        plt.xlabel('Books')
        plt.ylabel('Price (₹)')
        plt.title('Book Prices')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        tk.Button(self.root, text="Back to Home", command=self.book_selection_screen, font=("Helvetica", 12)).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
