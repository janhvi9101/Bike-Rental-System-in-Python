import csv
from tkinter import messagebox
import datetime

def sort_treeview(tree, col, reverse=False):
    l = [(tree.set(k,col), k) for k in tree.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
    except:
        l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree,col,not reverse))

def export_csv(filename, data, headers):
    with open(filename,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    messagebox.showinfo("Export Success", f"{filename} exported successfully!")

def notify_low_stock(db):
    db.cursor.execute("SELECT model, available_count FROM bikes WHERE available_count <=2")
    for model, count in db.cursor.fetchall():
        messagebox.showwarning("Low Stock Alert", f"Only {count} {model} bike(s) left!")

def notify_overdue(db):
    now = datetime.datetime.now()
    db.cursor.execute("SELECT user_name, bike_count, rent_type, rent_time FROM rentals WHERE return_time IS NULL")
    for user, count, rtype, rent_time in db.cursor.fetchall():
        rent_dt = datetime.datetime.fromisoformat(rent_time)
        duration_hours = (now - rent_dt).total_seconds()/3600
        if (rtype=="hour" and duration_hours>24) or (rtype=="day" and duration_hours>48):
            messagebox.showwarning("Overdue Rental", f"{user} has {count} overdue {rtype} rental(s)!")
