import tkinter as tk
from tkinter import messagebox
import csv
import os

# this list holds every item as [name, borrower, due date, status]
items = []

 # simple check that the date looks like dd/mm/yyyy
    # splits the text by "/" and checks there are 3 parts with the right lengths
    # also checks each part is actually a number, not letters or symbols

def is_valid_date(date_text):
   
    parts = date_text.split("/")
    if len(parts) != 3:
        return False
    day, month, year = parts
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return False
    if len(day) == 2 and len(month) == 2 and len(year) == 4:
        if 1 <= int(day) <= 31 and 1 <= int(month) <= 12:
            return True
    return False

def load_data():
    # loads items from the csv file if it exists
    # if something goes wrong reading the file, show an error instead of crashing
    if os.path.exists("resources.csv"):
        try:
            with open("resources.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    items.append(row)
        except:
            messagebox.showerror("Error", "could not load saved data")

def save_data():
    # saves the items list to the csv file
    try:
        with open("resources.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name","borrower","due","status"])
            for i in items:
                writer.writerow(i)
    except:
        messagebox.showerror("Error", "could not save data")

def refresh():
    # clears the list box and shows all items again, coloured by status
    listbox.delete(0, tk.END)
    for i in items:
        listbox.insert(tk.END, i[0] + "   " + i[1] + "   " + i[2] + "   " + i[3])
        if i[3] == "Available":
            listbox.itemconfig(tk.END, fg="green")
        else:
            listbox.itemconfig(tk.END, fg="orange")

def add_item():
    # adds a new item, checking the name isn't blank or already used
    # strip() removes extra spaces the user might have typed by accident
    name = name_entry.get().strip()
    if name == "":
        messagebox.showerror("Error", "type a name")
        return
    for i in items:
        if i[0].lower() == name.lower():
            messagebox.showerror("Error", "already exists")
            return
    items.append([name, "", "", "Available"])
    save_data()
    refresh()
    status_label.config(text="Item added successfully")

def borrow_item():
    # marks an item as borrowed, checking borrower and due date are filled in properly
    name = name_entry.get().strip()
    borrower = borrower_entry.get().strip()
    due = due_entry.get().strip()

    if borrower == "":
        messagebox.showerror("Error", "type a borrower name")
        return
    if due == "":
        messagebox.showerror("Error", "enter a due date")
        return
    if is_valid_date(due) == False:
        messagebox.showerror("Error", "due date must be in dd/mm/yyyy format")
        return

    found = False
    for i in items:
        if i[0].lower() == name.lower():
            found = True
            if i[3] == "Borrowed":
                messagebox.showerror("Error", "already borrowed")
                return
            i[1] = borrower
            i[2] = due
            i[3] = "Borrowed"
    if found == False:
        messagebox.showerror("Error", "item not found")
        return

    save_data()
    refresh()
    status_label.config(text="Item borrowed successfully")

def return_item():
    # marks a borrowed item as available again
    name = name_entry.get().strip()
    found = False
    for i in items:
        if i[0].lower() == name.lower():
            found = True
            if i[3] == "Available":
                messagebox.showerror("Error", "not borrowed")
                return
            i[1] = ""
            i[2] = ""
            i[3] = "Available"
    if found == False:
        messagebox.showerror("Error", "item not found")
        return

    save_data()
    refresh()
    status_label.config(text="Item returned successfully")

def search_item():
    # shows items where the keyword matches the item name or borrower
    keyword = search_entry.get().strip().lower()
    listbox.delete(0, tk.END)
    count = 0
    for i in items:
        if keyword in i[0].lower() or keyword in i[1].lower():
            listbox.insert(tk.END, i[0] + "   " + i[1] + "   " + i[2] + "   " + i[3])
            if i[3] == "Available":
                listbox.itemconfig(tk.END, fg="green")
            else:
                listbox.itemconfig(tk.END, fg="orange")
            count = count + 1
    status_label.config(text=str(count) + " results found")

def select_item(event):
    # fills the name box when a row is clicked
    # uses the row number to look up the item directly, so item names
    # with more than one word (like "Tool Box") still work
    selection = listbox.curselection()
    if not selection:
        return
    index = selection[0]
    name_entry.delete(0, tk.END)
    name_entry.insert(0, items[index][0])

def format_date_entry(event):
    # runs every time the user types in the due date box
    # keeps only the numbers typed, then adds the slashes back in automatically
    text = due_entry.get()
    digits = ""
    for ch in text:
        if ch.isdigit():
            digits = digits + ch
    digits = digits[:8]

    new_text = digits
    if len(digits) > 4:
        new_text = digits[0:2] + "/" + digits[2:4] + "/" + digits[4:]
    elif len(digits) > 2:
        new_text = digits[0:2] + "/" + digits[2:]

    due_entry.delete(0, tk.END)
    due_entry.insert(0, new_text)

window = tk.Tk()
window.title("Resource Tracker")
window.geometry("420x580")
window.config(bg="#1e1e1e")

title = tk.Label(window, text="Resource Tracker", bg="#1e1e1e", fg="white", font=("Arial", 14, "bold"))
title.pack(pady=10)

tk.Label(window, text="Item name", bg="#1e1e1e", fg="white").pack(anchor="w", padx=20)
name_entry = tk.Entry(window, font=("Arial", 12))
name_entry.pack(fill="x", padx=20, pady=5)

row1 = tk.Frame(window, bg="#1e1e1e")
row1.pack(fill="x", padx=20, pady=5)

col1 = tk.Frame(row1, bg="#1e1e1e")
col1.pack(side="left", expand=True, fill="x", padx=(0,5))
tk.Label(col1, text="Borrower", bg="#1e1e1e", fg="white").pack(anchor="w")
borrower_entry = tk.Entry(col1, font=("Arial", 12))
borrower_entry.pack(fill="x")

col2 = tk.Frame(row1, bg="#1e1e1e")
col2.pack(side="left", expand=True, fill="x")
tk.Label(col2, text="Due date (dd/mm/yyyy)", bg="#1e1e1e", fg="white").pack(anchor="w")
due_entry = tk.Entry(col2, font=("Arial", 12))
due_entry.pack(fill="x")
due_entry.bind("<KeyRelease>", format_date_entry)

row2 = tk.Frame(window, bg="#1e1e1e")
row2.pack(fill="x", padx=20, pady=10)
tk.Button(row2, text="Add", command=add_item).pack(side="left", expand=True, fill="x", padx=2)
tk.Button(row2, text="Borrow", command=borrow_item).pack(side="left", expand=True, fill="x", padx=2)
tk.Button(row2, text="Return", command=return_item).pack(side="left", expand=True, fill="x", padx=2)

tk.Label(window, text="Search item or borrower", bg="#1e1e1e", fg="white").pack(anchor="w", padx=20, pady=(10,0))
row3 = tk.Frame(window, bg="#1e1e1e")
row3.pack(fill="x", padx=20, pady=5)
search_entry = tk.Entry(row3, font=("Arial", 12))
search_entry.pack(side="left", expand=True, fill="x", padx=(0,5))
tk.Button(row3, text="Search", command=search_item).pack(side="left")

tk.Label(window, text="Click a row to select it", bg="#1e1e1e", fg="gray").pack(anchor="w", padx=20, pady=(10,0))

listbox = tk.Listbox(window, font=("Arial", 11), bg="white")
listbox.pack(fill="both", expand=True, padx=20, pady=5)
listbox.bind("<<ListboxSelect>>", select_item)

status_label = tk.Label(window, text="", bg="#1e1e1e", fg="lightblue")
status_label.pack(pady=5)

load_data()
refresh()

window.mainloop()