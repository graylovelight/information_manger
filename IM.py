import IM_Init
import Cryptography_Init
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image


def mainPasswordKeeper(username):
    root = Tk()
    root.title("欢迎您的到来! - 这里是个人信息管理器")
    root.iconbitmap("Static/IM.ico")
    width = 500
    height = 300
    root.geometry(str(width) + "x" + str(height))
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    root.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

    welcome_label = Label(root, text="Nice to meet you, " + username + ".", font=("Times New Roman", 30))
    welcome_label.grid(row=1, column=1, columnspan=50, padx=10, pady=10)

    def view():
        try:
            key = Cryptography_Init.get_key(username)
            root.destroy()
            IM_Init.show_all(key, username)
        except Exception as error:
            messagebox.showerror("Error", error)
            print(error)

    def add():
        try:
            IM_Init.createTable(username)
        except sqlite3.OperationalError:
            pass

        try:
            root.withdraw()
            add_new = Tk()
            add_new.title("添加新条目")
            add_new.iconbitmap("Static/IM.ico")
            width2 = 800
            height2 = 500
            add_new.geometry(str(width2) + "x" + str(height2))
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x_coordinate2 = int((screen_width / 2) - (width2 / 2))
            y_coordinate2 = int((screen_height / 2) - (height2 / 2))
            add_new.geometry(str(width2) + "x" + str(height2) + "+" + str(x_coordinate2) + "+" + str(y_coordinate2))

            info1_label = Label(add_new, text="请输入标题 (必填，可通过它搜索此记录)", font=("宋体", 14))
            info1_label.grid(row=0, column=0, pady=10)
            title_label = Label(add_new, text="Title:", font=("Times New Roman", 12))
            title_label.grid(row=1, column=0, pady=10)
            info2_label = Label(add_new, text="请输入内容(必填)", font=("宋体", 14))
            info2_label.grid(row=2, column=0, pady=10)
            content1_label = Label(add_new, text="Content", font=("Times New Roman", 12))
            content1_label.grid(row=3, column=0, pady=10)
            info3_label = Label(add_new, text="请输入概要 (选填)", font=("宋体", 14))
            info3_label.grid(row=6, column=0, pady=10)
            summary_label = Label(add_new, text="Summary:", font=("Times New Roman", 12))
            summary_label.grid(row=7, column=0, pady=10)
            info4_label = Label(add_new, text="请输入自用索引(选填，可通过它搜索此记录)", font=("宋体", 14))
            info4_label.grid(row=8, column=0, pady=10)
            index_label = Label(add_new, text="Index:", font=("Times New Roman", 12))
            index_label.grid(row=9, column=0, pady=10)

            title_entry = Entry(add_new, width=50)
            title_entry.grid(row=1, column=1)
            content1_entry = Entry(add_new, width=50)
            content1_entry.grid(row=3, column=1, ipady=10)
            summary_entry = Entry(add_new, width=50)
            summary_entry.grid(row=7, column=1)
            index_entry = Entry(add_new, width=50)
            index_entry.grid(row=9, column=1)

            def submit_add():
                encrypted_info = Cryptography_Init.encrypt_all(username, title_entry.get(), content1_entry.get(),
                                                               summary_entry.get(), index_entry.get())
                IM_Init.add_one(username, encrypted_info[0], encrypted_info[1], encrypted_info[2],
                                      encrypted_info[3])
                messagebox.showinfo(title="添加成功!", message="已成功添加新条目")
                title_entry.delete(0, END)
                content1_entry.delete(0, END)
                summary_entry.delete(0, END)
                index_entry.delete(0, END)

            def go_back():
                add_new.destroy()
                root.deiconify()

            submit_btn = Button(add_new, text="Add", command=submit_add)
            submit_btn.grid(row=10, column=0, pady=10)
            return_btn = Button(add_new, text="Return", command=go_back)
            return_btn.grid(row=10, column=1, pady=10)

        except Exception as error:
            messagebox.showerror("Error", error)

        add_new.mainloop()

    def search():
        top = Toplevel()
        top.title("~~搜索界面~~")
        top.iconbitmap("Static/IM.ico")
        width = 700
        height = 250
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        top.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

        try:
            clicked = StringVar()
            clicked.set("请选择一种搜索方式")
            drop = OptionMenu(top, clicked, "ID", "Title", "Index")
            drop.config(font=("Microsoft YaHei", 15))
            drop.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
            search_entry = Entry(top, width=28, font=("Microsoft YaHei", 12))
            search_entry.grid(row=0, column=2, padx=20, pady=20, columnspan=2)

            def perform_search():
                search_result = search_entry.get()
                if search_result == "":
                    messagebox.showerror("Error", "搜索栏不应该为空")
                    return
                key = Cryptography_Init.get_key(username)
                if clicked.get() == "ID":
                    IM_Init.id_lookup(key, username, search_entry.get())
                elif clicked.get() == "Title":
                    IM_Init.title_lookup(key, username, search_entry.get())
                elif clicked.get() == "Index":
                    IM_Init.index_lookup(key, username, search_entry.get())
                else:
                    messagebox.showerror("Error", "无效的输入，请重新尝试.")

            search_btn = Button(top, text="开始搜索", command=perform_search, font=("Microsoft YaHei", 15))
            search_btn.grid(row=1, column=0, padx=20, pady=20, columnspan=4)

            def go_back():
                top.destroy()

            return_btn = Button(top, text="返回", command=go_back, font=("Microsoft YaHei", 15))
            return_btn.grid(row=3, column=0, padx=20, pady=20, columnspan=4)

            top.mainloop()

        except Exception as error:
            print(error)

    def exit_program():
        root.destroy()
        bye = Tk()
        bye.title("下次再见!")
        bye.iconbitmap("Static/IM.ico")
        width = 800
        height = 500
        bye.geometry(str(width) + "x" + str(height))
        screen_width = bye.winfo_screenwidth()
        screen_height = bye.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        bye.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))
        my_img = ImageTk.PhotoImage(Image.open("Static/IM.png"))
        my_label = Label(bye, image=my_img)
        my_label.pack()
        quit_button = Button(bye, text="Exit", command=bye.destroy)
        quit_button.pack()
        bye.mainloop()

    view_pass_btn = Button(root, text="浏览条目", font=("Microsoft YaHei", 15), command=view)
    view_pass_btn.grid(row=3, column=1, padx=12, pady=10)
    add_pass_btn = Button(root, text="添加新条目", font=("Microsoft YaHei", 15), command=add)
    add_pass_btn.grid(row=3, column=5, padx=12, pady=10)
    search_pass_btn = Button(root, text="搜索和编辑特定条目", font=("KaiTi", 15), command=search)
    search_pass_btn.grid(row=5, column=3, columnspan=2, padx=12, pady=12)
    exit_btn = Button(root, text="离开", bg="white", fg="blue", font=("Times New Roman", 14), command=exit_program)
    exit_btn.grid(row=8, column=3, columnspan=2, pady=10)

    root.mainloop()
