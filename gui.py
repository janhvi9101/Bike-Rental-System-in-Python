import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from customer import Customer
from admin import Admin
from utils import notify_low_stock, notify_overdue
import datetime

class BikeRentalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚴 Bike Rental System")
        self.root.geometry("650x550")

        # Database and modules
        self.db = Database()
        self.customer = Customer(self.db)
        self.admin = Admin(self.db)

        # Header
        header_frame = tk.Frame(root, bg='#d1e7dd', pady=15)
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="🚴 Bike Rental System", font=('Helvetica', 20, 'bold'), bg='#d1e7dd').pack()

        # Dashboard frame
        self.dashboard_frame = tk.Frame(root, padx=20, pady=10, bg='#e8f6f3')
        self.dashboard_frame.pack(fill='x')
        self.update_dashboard()

        # Main buttons
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Button(main_frame, text="Rent a Bike", width=25, command=self.rent_bike_window).pack(pady=10)
        ttk.Button(main_frame, text="Return a Bike", width=25, command=self.return_bike_window).pack(pady=10)
        ttk.Button(main_frame, text="Check Inventory", width=25, command=self.show_inventory).pack(pady=10)
        ttk.Button(main_frame, text="Admin Login", width=25, command=self.admin_login_window).pack(pady=10)
        ttk.Button(main_frame, text="Exit", width=25, command=root.quit).pack(pady=10)

        # Notifications
        notify_low_stock(self.db)
        notify_overdue(self.db)

    # =========================
    # Dashboard
    # =========================
    def update_dashboard(self):
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        # Total Bikes
        self.db.cursor.execute("SELECT SUM(available_count) FROM bikes")
        total_bikes = self.db.cursor.fetchone()[0] or 0
        # Active Rentals
        self.db.cursor.execute("SELECT SUM(bike_count) FROM rentals WHERE return_time IS NULL")
        active_rentals = self.db.cursor.fetchone()[0] or 0
        # Total Revenue
        self.db.cursor.execute("SELECT SUM(bill) FROM rentals WHERE bill IS NOT NULL")
        revenue = self.db.cursor.fetchone()[0] or 0

        card_style = {'font': ('Helvetica', 14, 'bold'), 'bg': '#d1e7dd', 'width': 20, 'padx': 10, 'pady': 10}
        tk.Label(self.dashboard_frame, text=f"Total Bikes Available: {total_bikes}", **card_style).pack(side='left', padx=10, pady=5)
        tk.Label(self.dashboard_frame, text=f"Active Rentals: {active_rentals}", **card_style).pack(side='left', padx=10, pady=5)
        tk.Label(self.dashboard_frame, text=f"Total Revenue: ${revenue}", **card_style).pack(side='left', padx=10, pady=5)

    # =========================
    # Rent Bike Window
    # =========================
    def rent_bike_window(self):
        win = tk.Toplevel(self.root)
        win.title("Rent a Bike")
        win.geometry("400x350")
        win.configure(bg="#f2f2f2")

        tk.Label(win, text="Your Name:", bg="#f2f2f2").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack(pady=5)

        tk.Label(win, text="Number of Bikes:", bg="#f2f2f2").pack(pady=5)
        count_entry = ttk.Entry(win)
        count_entry.pack(pady=5)

        tk.Label(win, text="Rental Type:", bg="#f2f2f2").pack(pady=5)
        rental_type = tk.StringVar(value="hour")
        ttk.Radiobutton(win, text="Hourly ($5/hr)", variable=rental_type, value="hour").pack()
        ttk.Radiobutton(win, text="Daily ($20/day)", variable=rental_type, value="day").pack()

        def confirm():
            name = name_entry.get()
            try:
                count = int(count_entry.get())
            except:
                messagebox.showerror("Error", "Enter a valid number")
                return
            if self.customer.rent_bike(name, count, rental_type.get()):
                win.destroy()
                self.update_dashboard()

        ttk.Button(win, text="Confirm", command=confirm).pack(pady=15)

    # =========================
    # Return Bike Window
    # =========================
    def return_bike_window(self):
        win = tk.Toplevel(self.root)
        win.title("Return a Bike")
        win.geometry("400x250")
        win.configure(bg="#f2f2f2")

        tk.Label(win, text="Your Name:", bg="#f2f2f2").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack(pady=5)

        def confirm():
            name = name_entry.get()
            if self.customer.return_bike(name):
                win.destroy()
                self.update_dashboard()

        ttk.Button(win, text="Return", command=confirm).pack(pady=15)

    # =========================
    # Show Inventory
    # =========================
    def show_inventory(self):
        win = tk.Toplevel(self.root)
        win.title("Bike Inventory")
        win.geometry("300x200")
        win.configure(bg="#f2f2f2")

        self.db.cursor.execute("SELECT model, available_count FROM bikes")
        bikes = self.db.cursor.fetchall()

        text = ""
        for model, count in bikes:
            text += f"{model}: {count} available\n"

        tk.Label(win, text=text, font=('Helvetica', 12), bg='#f2f2f2').pack(pady=10)

    # =========================
    # Admin Login Window
    # =========================
    def admin_login_window(self):
        win = tk.Toplevel(self.root)
        win.title("Admin Login")
        win.geometry("350x200")
        win.configure(bg="#f2f2f2")

        tk.Label(win, text="Username:", bg="#f2f2f2").pack(pady=5)
        username_entry = ttk.Entry(win)
        username_entry.pack(pady=5)
        tk.Label(win, text="Password:", bg="#f2f2f2").pack(pady=5)
        password_entry = ttk.Entry(win, show="*")
        password_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.admin.login(username, password):
                messagebox.showinfo("Success", "Admin login successful!")
                win.destroy()
                self.add_bike_window()

        ttk.Button(win, text="Login", command=login).pack(pady=10)

    # =========================
    # Admin Add Bike Window
    # =========================
    def add_bike_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Bike (Admin)")
        win.geometry("350x250")
        win.configure(bg="#f2f2f2")

        tk.Label(win, text="Bike Model:", bg="#f2f2f2").pack(pady=5)
        model_entry = ttk.Entry(win)
        model_entry.pack(pady=5)
        tk.Label(win, text="Available Count:", bg="#f2f2f2").pack(pady=5)
        count_entry = ttk.Entry(win)
        count_entry.pack(pady=5)
        tk.Label(win, text="Rate per Hour ($):", bg="#f2f2f2").pack(pady=5)
        rate_hour_entry = ttk.Entry(win)
        rate_hour_entry.pack(pady=5)
        tk.Label(win, text="Rate per Day ($):", bg="#f2f2f2").pack(pady=5)
        rate_day_entry = ttk.Entry(win)
        rate_day_entry.pack(pady=5)

        def confirm():
            try:
                count = int(count_entry.get())
                rate_hour = float(rate_hour_entry.get())
                rate_day = float(rate_day_entry.get())
                model = model_entry.get()
            except:
                messagebox.showerror("Error", "Enter valid numbers")
                return
            self.admin.add_bike(model, count, rate_hour, rate_day)
            win.destroy()
            self.update_dashboard()

        ttk.Button(win, text="Add Bike", command=confirm).pack(pady=10)
