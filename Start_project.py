import sqlite3
import hashlib
import win32api
import time
import random
import ctypes
from cryptography.fernet import Fernet
import Start_project_Init
import IM
import IM_Init
import Cryptography_Init
from tkinter import *
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk


def nop_sledding1():
    fake_var = random.randint(1, 100)
    for _ in range(random.randint(1, 10)):
        fake_var = (fake_var * random.randint(1, 10)) % random.randint(1, 10)
    if fake_var % 2 == 0:
        fake_var += 1
    else:
        fake_var -= 1
    return fake_var


def nop_sledding2():
    fake_var = random.randint(10, 50)
    for _ in range(random.randint(4, 10)):
        fake_var = (fake_var * random.randint(1, 10)) % random.randint(1, 10)
    if fake_var % 2 == 0:
        fake_var += 1
    else:
        fake_var -= 1
    return fake_var


# 检测调试器是否存在
def is_debugger_present():
    try:
        return ctypes.windll.kernel32.IsDebuggerPresent()
    except Exception as e:
        print(f"IsDebuggerPresent failed: {e}")
    return False


# 检查是否存在远程调试器
def check_remote_debugger_present():
    try:
        is_debugger_present_remote = ctypes.c_bool()
        ctypes.windll.kernel32.CheckRemoteDebuggerPresent(ctypes.windll.kernel32.GetCurrentProcess(),
                                                          ctypes.byref(is_debugger_present_remote))
        return is_debugger_present_remote.value
    except Exception as e:
        print(f"CheckRemoteDebuggerPresent failed: {e}")
    return False


# 检查调试寄存器
def check_debug_registers():
    class CONTEXT(ctypes.Structure):
        _fields_ = [("ContextFlags", ctypes.c_uint),
                    ("Dr0", ctypes.c_ulonglong),
                    ("Dr1", ctypes.c_ulonglong),
                    ("Dr2", ctypes.c_ulonglong),
                    ("Dr3", ctypes.c_ulonglong),
                    ("Dr6", ctypes.c_ulonglong),
                    ("Dr7", ctypes.c_ulonglong)]

    try:
        ctx = CONTEXT()
        ctx.ContextFlags = 0x10010
        hThread = ctypes.windll.kernel32.GetCurrentThread()
        if ctypes.windll.kernel32.GetThreadContext(hThread, ctypes.byref(ctx)):
            return ctx.Dr0 or ctx.Dr1 or ctx.Dr2 or ctx.Dr3 or ctx.Dr6 or ctx.Dr7
    except Exception as e:
        print(f"CheckDebugRegisters failed: {e}")
    return False


# 检查调试器附加
def check_debugger_attached():
    try:
        process_info = ctypes.Structure()
        status = ctypes.windll.ntdll.NtQueryInformationProcess(-1, 0, ctypes.byref(process_info),
                                                               ctypes.sizeof(process_info), None)
        if status == 0x00000000:
            return True
    except Exception as e:
        print(f"CheckDebuggerAttached failed: {e}")
    return False


# 检测运行时间异常
def check_time_anomaly():
    start = time.time()
    for _ in range(1000):
        pass
    end = time.time()
    if end - start > 0.05:
        return True
    return False


# 使用硬件断点检测
def check_hardware_breakpoints():
    try:
        ctypes.windll.kernel32.OutputDebugStringW("Debugging detection")
        if ctypes.windll.kernel32.GetLastError() == 0:
            return True
    except Exception as e:
        print(f"CheckHardwareBreakpoints failed: {e}")
    return False


# 主反调试函数
def anti_debug(check_all=True):
    if check_all:
        if is_debugger_present() or check_remote_debugger_present() or check_debug_registers() or check_debugger_attached() or check_time_anomaly() or check_hardware_breakpoints():
            messagebox.showerror("错误", "发现程序处于被调试状态，运行中止！")
            exit(-1)


# 反调试保护
try:
    anti_debug(0)
except Exception as e:
    print(f"Anti-debug protection failed: {e}")

root = Tk()
root.title("用户界面")
root.iconbitmap("Static/background.jpg")
width = 700
height = 600
root.geometry(f"{width}x{height}")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (width / 2))
y_coordinate = int((screen_height / 2) - (height / 2))
root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

canvas = Canvas(root, height=height, width=width)
background_image = ImageTk.PhotoImage(Image.open("Static/background.jpg"))
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
canvas.pack()

frame = Frame(root, bg='#f0f0f0', bd=5, relief='raised')
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.5, anchor='n')

welcome_label = Label(frame, text="个人信息管理应用", font=("楷体", 30))
welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
username_label = Label(frame, text="用户名:", font=("楷体", 15))
username_label.grid(row=1, column=0, padx=3, pady=10, sticky=W)
password_label = Label(frame, text="密码:", font=("楷体", 15))
password_label.grid(row=2, column=0, padx=3, pady=10, sticky=W)
license_label = Label(frame, text="授权码:", font=("楷体", 15))
license_label.grid(row=3, column=0, padx=3, pady=10, sticky=W)

username_entry = ttk.Combobox(frame, width=30)
username_entry.grid(row=1, column=1, padx=3, pady=10)
password_entry = Entry(frame, width=33, show="*")
password_entry.grid(row=2, column=1, padx=3, pady=10)
license_entry = Entry(frame, width=33)
license_entry.grid(row=3, column=1, padx=3, pady=10)


def get_hard_disk_serial():
    nop_sledding1()
    return win32api.GetVolumeInformation("C:\\")[1]


def get_cpu_serial():
    cpu = os.popen('wmic cpu get processorid').read()
    cpu = cpu.strip().replace('\n', '').replace('\r', '').split(" ")
    nop_sledding2()
    cpu = cpu[len(cpu) - 1]
    return cpu


def generate_salt():
    nop_sledding1()
    return int(time.time() // 3600)


def generate_key(username, serial_number, cpu_number, salt):
    user_hash = hashlib.sha256(username.encode()).hexdigest()
    nop_sledding2()
    combined_info = f"{serial_number}{cpu_number}{user_hash}{salt}"
    intermediate_key = int(hashlib.sha256(combined_info.encode()).hexdigest(), 16)
    final_key = intermediate_key ^ 0x42945178
    nop_sledding1()
    final_key = (final_key * 31) + len(username)
    return final_key


def validate_license(serial_number, username, user_key, cpu_number, salt):
    generated_key = generate_key(username, serial_number, cpu_number, salt)
    nop_sledding2()
    return generated_key == user_key


def is_user_blacklisted(username):
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    nop_sledding1()
    c.execute("SELECT * FROM blacklist WHERE username=?", (username,))
    blacklisted_user = c.fetchone()
    conn.close()
    return blacklisted_user is not None


def load_username_history():
    if os.path.exists('username_history.txt'):
        with open('username_history.txt', 'r') as file:
            usernames = file.read().splitlines()
            return usernames
    return []


def validate_admin(password, auth_code):
    admin_username, encrypted_admin_password = Start_project_Init.get_admin_credentials()
    if admin_username is None or encrypted_admin_password is None:
        return False

    key = Cryptography_Init.get_key(admin_username)
    nop_sledding1()
    f = Fernet(key)
    decrypted_pass = f.decrypt(encrypted_admin_password).decode()

    return decrypted_pass == password and admin_username == auth_code


username_history = load_username_history()
username_entry['values'] = username_history


def save_username_to_history(username):
    with open('username_history.txt', 'a') as file:
        file.write(username + '\n')


def login():
    if username_entry.get() == "" or password_entry.get() == "" or license_entry.get() == "":
        messagebox.showwarning("警告", "用户名、密码与授权码皆不可为空!")
    else:
        username = username_entry.get()
        password = password_entry.get()
        user_key = int(license_entry.get())
        nop_sledding1()

        if is_user_blacklisted(username):
            messagebox.showerror("发生错误", "该用户已被列入黑名单，无法登录")
            return

        serial_number = get_hard_disk_serial()
        cpu_number = get_cpu_serial()
        salt = generate_salt()

        if not validate_license(serial_number, username, user_key, cpu_number, salt):
            messagebox.showerror("发生错误", "无效的授权码！请再次尝试")
            return
        try:
            key = Cryptography_Init.get_key(username)
            if Start_project_Init.searchUser(key, username, password):
                root.destroy()
                IM.mainPasswordKeeper(username)
            else:
                messagebox.showerror("发生错误", "用户名或密码错误！请再次尝试")
        except Exception as error:
            messagebox.showerror("Error", error)


def signup():
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showwarning("警告", "用户名与密码皆不可为空!!")
    else:
        username = username_entry.get()
        password = password_entry.get()

        try:
            conn = sqlite3.connect("PM.db")
            c = conn.cursor()

            try:
                Start_project_Init.tableCreate()
            except sqlite3.OperationalError as error:
                messagebox.showwarning("Error", error)

            c.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = c.fetchone()

            if existing_user:
                messagebox.showwarning("Error", "该用户名已经存在")
                return

            Cryptography_Init.set_key(username)
            encrypted_user = Cryptography_Init.encrypt_some(username, password)
            encrypted_password = encrypted_user[1]
            Start_project_Init.signup(username, encrypted_password)
            IM_Init.createTable(username)
            save_username_to_history(username)
            root.destroy()
            IM.mainPasswordKeeper(username)
        except sqlite3.OperationalError as error:
            messagebox.showwarning("Error", error)
        except Exception as error:
            messagebox.showwarning("Error", error)
        finally:
            conn.close()


def add_user_to_blacklist(username):
    conn = sqlite3.connect("PM.db")
    c = conn.cursor()
    c.execute("INSERT INTO blacklist (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()


def add_to_blacklist():
    username_to_blacklist = username_entry.get()
    admin_password = password_entry.get()
    admin_auth_code = license_entry.get()

    if username_to_blacklist and admin_password and admin_auth_code:
        if validate_admin(admin_password, admin_auth_code):
            add_user_to_blacklist(username_to_blacklist)
            messagebox.showinfo("成功", f"用户 {username_to_blacklist} 已被添加到黑名单")
        else:
            messagebox.showerror("错误", "管理员密码或暗号错误，无法将用户加入黑名单")
    else:
        messagebox.showwarning("警告", "请输入用户名、管理员密码和暗号")


def info():
    os.system('notepad Static/帮助.txt')


login_button = Button(frame, text="登录", font=("楷体", 13), command=login)
login_button.grid(row=4, column=0, pady=15)
signup_button = Button(frame, text="注册", font=("楷体", 13), command=signup)
signup_button.grid(row=4, column=1, pady=15)
blacklist_button = Button(frame, text="加入黑名单", font=("楷体", 13), command=add_to_blacklist)
blacklist_button.grid(row=4, column=2, columnspan=2, pady=15)
info_button = Button(root, text="帮助", font=("楷体", 13), command=info)
info_button.place(relx=0.9, rely=0.02, anchor='ne')

root.mainloop()
