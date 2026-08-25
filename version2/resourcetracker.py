import tkinter as tk
from tkinter import messagebox
import csv
import os

items = []

def load_data():
    if os.path.exists("resources.csv"):
        with open("resources.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                items.append(row)

def save_data():
    with open("resources.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name","borrower","due","status"])
        for i in items:
            writer.writerow(i)

def refresh():
    listbox.delete(0, tk.END)
    for i in items:
        listbox.insert(tk.END, i[0] + "   " + i[1] + "   " + i[2] + "   " + i[3])

def add_item():
    name = name_entry.get()
    if name == "":
        messagebox.showerror("Error", "type a name")
        return
    for i in items:
        if i[0] == name:
            messagebox.showerror("Error", "already exists")
            return
    items.append([name, "", "", "Available"])
    save_data()
    refresh()
    status_label.config(text="Item added successfully")

def borrow_item():
    name = name_entry.get()
    borrower = borrower_entry.get()
    due = due_entry.get()
    if borrower == "":
        messagebox.showerror("Error", "type a borrower name")
        return
    found = False
    for i in items:
        if i[0] == name:
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
    name = name_entry.get()
    found = False
    for i in items:
        if i[0] == name:
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
    keyword = search_entry.get().lower()
    listbox.delete(0, tk.END)
    if keyword == "":
        refresh()
        return
    for i in items:
        if keyword in i[0].lower() or keyword in i[1].lower():
            listbox.insert(tk.END, i[0] + "   " + i[1] + "   " + i[2] + "   " + i[3])

def select_item(event):
    selection = listbox.curselection()
    if not selection:
        return
    line = listbox.get(selection[0])
    parts = line.split()
    name_entry.delete(0, tk.END)
    name_entry.insert(0, parts[0])

window = tk.Tk()
window.title("Resource Tracker")
window.geometry("420x560")
window.config(bg="#1e1e1e")

title = tk.Label(window, text="Resource Tracker — v2", bg="#1e1e1e", fg="white", font=("Arial", 14, "bold"))
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
tk.Label(col2, text="Due date", bg="#1e1e1e", fg="white").pack(anchor="w")
due_entry = tk.Entry(col2, font=("Arial", 12))
due_entry.pack(fill="x")

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

listbox = tk.Listbox(window, font=("Arial", 11))
listbox.pack(fill="both", expand=True, padx=20, pady=5)
listbox.bind("<<ListboxSelect>>", select_item)

status_label = tk.Label(window, text="", bg="#1e1e1e", fg="lightgreen")
status_label.pack(pady=5)

load_data()
refresh()

window.mainloop()
