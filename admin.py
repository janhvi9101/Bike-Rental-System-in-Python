from tkinter import messagebox

class Admin:
    def __init__(self, db):
        self.db = db

    def login(self, username, password):
        self.db.cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username,password))
        if self.db.cursor.fetchone():
            return True
        else:
            messagebox.showerror("Error","Invalid credentials")
            return False

    def add_bike(self, model, count, rate_hour, rate_day):
        self.db.cursor.execute("INSERT INTO bikes (model, available_count, rate_hour, rate_day) VALUES (?,?,?,?)",
                               (model,count,rate_hour,rate_day))
        self.db.conn.commit()
        messagebox.showinfo("Success", f"{count} {model} bike(s) added!")
