import tkinter as tk
from tkinter import messagebox

items = [] 

def add_item():
    name = name_entry.get()
    if name == "":
        messagebox.showerror("Error", "Enter an item name")
        return
    items.append([name, "", "Available"])
    show_items()

def borrow_item():
    name = name_entry.get()
    borrower = borrower_entry.get()
    for i in items:
        if i[0] == name and i[2] == "Available":
            i[1] = borrower
            i[2] = "Borrowed"
            show_items()
            return
    messagebox.showerror("Error", "Item not found or already borrowed")

def return_item():
    name = name_entry.get()
    for i in items:
        if i[0] == name and i[2] == "Borrowed":
            i[1] = ""
            i[2] = "Available"
            show_items()
            return
    messagebox.showerror("Error", "Item not found or not borrowed")

def search_item():
    keyword = name_entry.get().lower()
    listbox.delete(0, tk.END)
    for i in items:
        if keyword in i[0].lower():
            listbox.insert(tk.END, i[0] + " - " + i[1] + " - " + i[2])

def show_items():
    listbox.delete(0, tk.END)
    for i in items:
        listbox.insert(tk.END, i[0] + " - " + i[1] + " - " + i[2])

window = tk.Tk()
window.title("Resource Tracker")

tk.Label(window, text="Item name:").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Borrower:").pack()
borrower_entry = tk.Entry(window)
borrower_entry.pack()

tk.Button(window, text="Add", command=add_item).pack()
tk.Button(window, text="Borrow", command=borrow_item).pack()
tk.Button(window, text="Return", command=return_item).pack()
tk.Button(window, text="Search", command=search_item).pack()
tk.Button(window, text="Show all", command=show_items).pack()

listbox = tk.Listbox(window, width=50)
listbox.pack(pady=10)

window.mainloop()