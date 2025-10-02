import datetime
from tkinter import messagebox

class Customer:
    def __init__(self, db):
        self.db = db

    def rent_bike(self, name, count, rental_type):
        self.db.cursor.execute("SELECT available_count FROM bikes WHERE model=?", ("Standard",))
        available = self.db.cursor.fetchone()[0]
        if count <=0 or count > available:
            messagebox.showerror("Error","Not enough bikes available")
            return False
        self.db.cursor.execute("UPDATE bikes SET available_count=available_count-? WHERE model=?", (count,"Standard"))
        self.db.cursor.execute("""INSERT INTO rentals (user_name, bike_model, bike_count, rent_type, rent_time, return_time, bill)
                                  VALUES (?,?,?,?,?,NULL,NULL)""",
                               (name,"Standard",count,rental_type,datetime.datetime.now().isoformat()))
        self.db.conn.commit()
        messagebox.showinfo("Success", f"{name} rented {count} bike(s)")
        return True

    def return_bike(self, name):
        self.db.cursor.execute("SELECT id, bike_count, rent_time, rent_type FROM rentals WHERE user_name=? AND return_time IS NULL", (name,))
        rental = self.db.cursor.fetchone()
        if not rental:
            messagebox.showerror("Error", "No active rental found")
            return False
        rental_id, count, rent_time, rtype = rental
        rent_time = datetime.datetime.fromisoformat(rent_time)
        duration_hours = (datetime.datetime.now() - rent_time).total_seconds()/3600
        bill = round(5*count*duration_hours,2) if rtype=="hour" else 20*count*max(1,duration_hours//24)
        self.db.cursor.execute("UPDATE rentals SET return_time=?, bill=? WHERE id=?", (datetime.datetime.now().isoformat(), bill, rental_id))
        self.db.cursor.execute("UPDATE bikes SET available_count=available_count+? WHERE model=?", (count,"Standard"))
        self.db.conn.commit()
        messagebox.showinfo("Bill", f"{name}, your bill is ${bill}")
        return True
