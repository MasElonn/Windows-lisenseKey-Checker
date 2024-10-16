import tkinter as tk
from tkinter import messagebox
import winreg

def get_windows_product_key():
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    value_name = "DigitalProductId"

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(registry_key, value_name)
        winreg.CloseKey(registry_key)
        
        # Decrypt the product key from the registry
        key = decode_product_key(value)
        return key
    except WindowsError as e:
        messagebox.showerror("Error", f"Error accessing registry: {e}")
        return None

def decode_product_key(digital_product_id):
    key = ''
    key_offset = 52
    is_win8 = (digital_product_id[66] >> 3) & 1
    if is_win8:
        digital_product_id = digital_product_id[key_offset:key_offset + 15]
        decode_length = 29
        decode_string = list('BCDFGHJKMPQRTVWXY2346789')
    else:
        digital_product_id = digital_product_id[key_offset:key_offset + 15]
        decode_length = 25
        decode_string = list('BCDFGHJKMPQRTVWXY2346789')
        
    digital_product_id = list(digital_product_id)  # Convert to list for mutability
    
    last = 0
    for i in range(decode_length):
        current = 0
        for j in range(14, -1, -1):
            current = current * 256
            current = digital_product_id[j] + current
            digital_product_id[j] = (current // len(decode_string))
            current = current % len(decode_string)
        last = current
        key = decode_string[current] + key
        if (i + 1) % 6 == 0 and i != decode_length - 1:
            key = '-' + key
    return key

def show_product_key():
    product_key = get_windows_product_key()
    if product_key:
        messagebox.showinfo("Windows Product Key", f"Your Windows product key: {product_key}")
    else:
        messagebox.showerror("Error", "Unable to find the Windows product key.")

# Create the graphical user interface
root = tk.Tk()
root.title("Windows Product Key Checker")
root.geometry("300x100")

btn_check_key = tk.Button(root, text="Get Product Key", command=show_product_key)
btn_check_key.pack(pady=20)

root.mainloop()
