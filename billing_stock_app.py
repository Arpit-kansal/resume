import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3

def get_stock_data():
    conn = sqlite3.connect('billing_stock.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_stock():
    item_name = entry_item_name.get()
    quantity = int(entry_quantity.get())
    price = float(entry_price.get())
    
    conn = sqlite3.connect('billing_stock.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock (item_name, quantity, price) VALUES (?, ?, ?)", (item_name, quantity, price))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Item added to stock")
    entry_item_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    update_stock_list()

def update_stock_list():
    for item in stock_list.get_children():
        stock_list.delete(item)
        
    for row in get_stock_data():
        stock_list.insert("", tk.END, values=row)

def create_bill():
    item_id = int(entry_bill_item_id.get())
    quantity = int(entry_bill_quantity.get())

def print():
    item_id = int(entry_bill_item_id.get())
    quantity = int(entry_bill_quantity.get())


    conn = sqlite3.connect('billing_stock.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT price, quantity FROM stock WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    if item and item[1] >= quantity:
        total_price = item[0] * quantity
        cursor.execute("INSERT INTO billing (item_id, quantity, total_price) VALUES (?, ?, ?)", (item_id, quantity, total_price))
        cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE id = ?", (quantity, item_id))
        conn.commit()
        messagebox.showinfo("Success", f"Bill created for ${total_price}")
    else:
        messagebox.showwarning("Error", "Insufficient stock")
    
    conn.close()
    entry_bill_item_id.delete(0, tk.END)
    entry_bill_quantity.delete(0, tk.END)
    update_stock_list()

# GUI Setup
root = tk.Tk()
root.title("Billing and Stock Management")

frame = tk.Frame(root)
frame.pack(pady=20)

# Stock Input
tk.Label(frame, text="Item Name").grid(row=0, column=0)
entry_item_name = tk.Entry(frame)
entry_item_name.grid(row=0, column=1)

tk.Label(frame, text="Quantity").grid(row=1, column=0)
entry_quantity = tk.Entry(frame)
entry_quantity.grid(row=1, column=1)

tk.Label(frame, text="Price").grid(row=2, column=0)
entry_price = tk.Entry(frame)
entry_price.grid(row=2, column=1)

tk.Button(frame, text="Add to Stock", command=add_stock).grid(row=3, columnspan=2)

# Stock List
stock_list = tk.ttk.Treeview(root, columns=("ID", "Item Name", "Quantity", "Price"), show='headings')
stock_list.heading("ID", text="ID")
stock_list.heading("Item Name", text="Item Name")
stock_list.heading("Quantity", text="Quantity")
stock_list.heading("Price", text="Price")
stock_list.pack(pady=20)
update_stock_list()

# Billing Input
frame_billing = tk.Frame(root)
frame_billing.pack(pady=20)

tk.Label(frame_billing, text="Item ID").grid(row=0, column=0)
entry_bill_item_id = tk.Entry(frame_billing)
entry_bill_item_id.grid(row=0, column=1)

tk.Label(frame_billing, text="Quantity").grid(row=1, column=0)
entry_bill_quantity = tk.Entry(frame_billing)
entry_bill_quantity.grid(row=1, column=1)

# tk.Label(frame_billing, text="Price").grid(row=1,column=0)



tk.Button(frame_billing, text="Create Bill", command=create_bill).grid(row=2, columnspan=2)
# tk.Button(frame_billing,text="Print", command=print).grid(row=3,columnspan=3)
root.mainloop()
