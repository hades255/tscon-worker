import psutil
import win32api
import win32process
import win32con
import os

def get_description(exe_path):
    try:
        lang, codepage = win32api.GetFileVersionInfo(exe_path, '\\VarFileInfo\\Translation')[0]
        str_info_path = f'\\StringFileInfo\\{lang:04x}{codepage:04x}\\FileDescription'
        return win32api.GetFileVersionInfo(exe_path, str_info_path)
    except:
        return ""

print("Processes with 'Microsoft® Windows®' in description:\n")

for proc in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        if not proc.info['exe']:
            continue
        desc = get_description(proc.info['exe'])
        if "Microsoft® Windows®" in desc:
            print(f"[{proc.info['pid']}] {proc.info['name']} — {desc}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
