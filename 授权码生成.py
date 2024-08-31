import os
import hashlib
import time
import win32api


def get_hard_disk_serial():
    return win32api.GetVolumeInformation("C:\\")[1]


def get_cpu_serial():
    cpu = os.popen('wmic cpu get processorid').read()
    cpu = cpu.strip().replace('\n', '').replace('\r', '').split(" ")
    cpu = cpu[len(cpu) - 1]
    return cpu


def generate_salt():
    return int(time.time() // 3600)  # 每小时变化一次的盐值


def generate_key(username, serial_number, cpu_number, salt):
    user_hash = hashlib.sha256(username.encode()).hexdigest()
    combined_info = f"{serial_number}{cpu_number}{user_hash}{salt}"
    intermediate_key = int(hashlib.sha256(combined_info.encode()).hexdigest(), 16)
    final_key = intermediate_key ^ 0x42945178
    final_key = (final_key * 31) + len(username)
    return final_key


def validate_license(serial_number, username, user_key, cpu_number, salt):
    generated_key = generate_key(username, serial_number, cpu_number, salt)
    return generated_key == user_key


serial_number = get_hard_disk_serial()
cpu_number = get_cpu_serial()
salt = generate_salt()
username = input("输入你的用户名: ")
generated_key = generate_key(username, serial_number, cpu_number, salt)
print(generated_key)
