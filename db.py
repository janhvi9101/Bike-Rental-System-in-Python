import sqlite3
import datetime

class Database:
    def __init__(self, db_name="bikerental.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bikes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                model TEXT,
                                available_count INTEGER,
                                rate_hour REAL,
                                rate_day REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_name TEXT,
                                bike_model TEXT,
                                bike_count INTEGER,
                                rent_type TEXT,
                                rent_time TEXT,
                                return_time TEXT,
                                bill REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                password TEXT)''')
        self.conn.commit()

        # Default data
        self.cursor.execute("SELECT COUNT(*) FROM bikes")
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO bikes (model, available_count, rate_hour, rate_day) VALUES (?,?,?,?)",
                                ("Standard",10,5,20))
        self.cursor.execute("SELECT COUNT(*) FROM admins")
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO admins (username,password) VALUES (?,?)",("admin","admin123"))
        self.conn.commit()
