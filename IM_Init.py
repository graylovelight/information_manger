import sqlite3
from tkinter import *
from tkinter import messagebox

from cryptography.fernet import Fernet

import IM


def show_all(key, username):
    f = Fernet(key)
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()

    root = Tk()
    root.title("您的信息:")
    root.iconbitmap("Static/IM.ico")
    width = 600
    height = 800
    root.geometry(f"{width}x{height}")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    sb = Scrollbar(root)
    sb.pack(side=RIGHT, fill=Y)
    mylist = Listbox(root, yscrollcommand=sb.set, width=width, height=(height - 20))

    for item in items:
        decrypted_title = f.decrypt(item[1]).decode()
        decrypted_content1 = f.decrypt(item[2]).decode()
        decrypted_summary = f.decrypt(item[3]).decode()
        decrypted_index = f.decrypt(item[4]).decode()
        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "Id: " + str(item[0]))
        mylist.insert(END, "Title: " + decrypted_title)
        mylist.insert(END, "Content1: " + decrypted_content1)
        mylist.insert(END, "Summary: " + decrypted_summary)
        mylist.insert(END, "Index: " + decrypted_index)
        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "")

    def go_back():
        root.destroy()
        IM.mainPasswordKeeper(username)

    Button(root, text="Return", command=go_back).pack()

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)
    conn.commit()
    conn.close()


def add_one(username, title, content1, summary, index):
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("INSERT INTO " + username + " VALUES (?, ?, ?, ?)", (title, content1, summary, index))
    conn.commit()
    conn.close()


def edit(key, username, id, new_title, new_content1, new_summary, new_index):
    f = Fernet(key)
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    encrypted_title = f.encrypt(new_title.encode())
    encrypted_content1 = f.encrypt(new_content1.encode())
    encrypted_summary = f.encrypt(new_summary.encode())
    encrypted_index = f.encrypt(new_index.encode())
    c.execute("UPDATE " + username + " SET title = ?, content1 = ?, summary = ?, index_info = ? WHERE rowid = ?",
              (encrypted_title, encrypted_content1, encrypted_summary, encrypted_index, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("修改成功", "修改后的内容已保持!")


def delete(key, username, id):
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("DELETE FROM " + username + " WHERE rowid = ?", (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("删除成功", "对应条目已删除!")


def display_search_results(key, username, items):
    f = Fernet(key)
    toplvl = Toplevel()
    toplvl.title("搜索的结果如下：")
    toplvl.iconbitmap("Static/IM.ico")
    width = 600
    height = 800
    screen_width = toplvl.winfo_screenwidth()
    screen_height = toplvl.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    toplvl.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    sb = Scrollbar(toplvl)
    sb.pack(side=RIGHT, fill=Y)
    mylist = Listbox(toplvl, yscrollcommand=sb.set, width=width, height=(height - 20))

    def edit_password_callback(item):
        edit_window = Toplevel()
        edit_window.title("Edit Record")
        edit_window.geometry("400x400")
        Label(edit_window, text="Title:").pack()
        entry_title = Entry(edit_window)
        entry_title.pack()
        entry_title.insert(0, item[1])
        Label(edit_window, text="Content1:").pack()
        entry_content1 = Entry(edit_window)
        entry_content1.pack()
        entry_content1.insert(0, item[2])
        Label(edit_window, text="Summary:").pack()
        entry_summary = Entry(edit_window)
        entry_summary.pack()
        entry_summary.insert(0, item[3])
        Label(edit_window, text="Index:").pack()
        entry_index = Entry(edit_window)
        entry_index.pack()
        entry_index.insert(0, item[4])

        def save_changes():
            new_title = entry_title.get()
            new_content1 = entry_content1.get()
            new_summary = entry_summary.get()
            new_index = entry_index.get()
            edit(key, username, item[0], new_title, new_content1, new_summary, new_index)
            edit_window.destroy()

        Button(edit_window, text="Save", command=save_changes).pack()

    def delete_password_callback(id):
        if messagebox.askyesno("删除", "您确定要删除该条目吗?"):
            delete(key, username, id)
            toplvl.destroy()

    for item in items:
        decrypted_title = f.decrypt(item[1]).decode()
        decrypted_content1 = f.decrypt(item[2]).decode()
        decrypted_summary = f.decrypt(item[3]).decode()
        decrypted_index = f.decrypt(item[4]).decode()
        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "Id: " + str(item[0]))
        mylist.insert(END, "Title: " + decrypted_title)
        mylist.insert(END, "Content1: " + decrypted_content1)
        mylist.insert(END, "Summary: " + decrypted_summary)
        mylist.insert(END, "Index: " + decrypted_index)
        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "")
        Button(toplvl, text="Edit", command=lambda item=item: edit_password_callback(
            (item[0], decrypted_title, decrypted_content1, decrypted_summary, decrypted_index))).pack()
        Button(toplvl, text="Delete", command=lambda id=item[0]: delete_password_callback(id)).pack()

    def go_back():
        toplvl.destroy()

    Button(toplvl, text="Return", command=go_back).pack()
    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)
    toplvl.mainloop()


def title_lookup(key, username, title):
    f = Fernet(key)
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()
    filtered_items = [item for item in items if f.decrypt(item[1]).decode() == title]
    display_search_results(key, username, filtered_items)
    conn.commit()
    conn.close()


def index_lookup(key, username, index):
    f = Fernet(key)
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()
    filtered_items = [item for item in items if f.decrypt(item[4]).decode() == index]
    display_search_results(key, username, filtered_items)
    conn.commit()
    conn.close()


def id_lookup(key, username, id):
    f = Fernet(key)
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM " + username + " WHERE rowid = ?", (id,))
    items = c.fetchall()
    display_search_results(key, username, items)
    conn.commit()
    conn.close()


def createTable(username):
    connection = sqlite3.connect("PM.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE " + username + "(title text, content1 text, summary text, index_info text)")
    connection.commit()
    connection.close()
