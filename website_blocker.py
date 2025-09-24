import os
import sys
import ctypes
from tkinter import *
from tkinter import messagebox

# --- Ask for Admin Rights ---
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Relaunch the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

run_as_admin()

# --- Config ---
host_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"


def block_websites():
    websites = text_area.get("1.0", END).splitlines()
    websites = [site.strip() for site in websites if site.strip()]

    if not websites:
        messagebox.showwarning("Warning", "No websites entered!")
        return

    with open(host_path, 'r+') as host_file:
        content = host_file.read()
        for site in websites:
            if site not in content:
                host_file.write(redirect + " " + site + "\n")

    messagebox.showinfo("Success", "Websites Blocked!")


def unblock_websites():
    websites = text_area.get("1.0", END).splitlines()
    websites = [site.strip() for site in websites if site.strip()]

    if not websites:
        messagebox.showwarning("Warning", "No websites entered!")
        return

    with open(host_path, 'r+') as host_file:
        lines = host_file.readlines()
        host_file.seek(0)
        for line in lines:
            if not any(site in line for site in websites):
                host_file.write(line)
        host_file.truncate()

    messagebox.showinfo("Success", "Websites Unblocked!")


# --- Tkinter UI ---
root = Tk()
root.title("Website Blocker")
root.geometry("400x400")
root.resizable(False, False)

label = Label(root, text="Enter Websites (one per line):", font=("Arial", 12))
label.pack(pady=10)

text_area = Text(root, height=10, width=40, font=("Arial", 10))
text_area.pack(pady=5)

frame = Frame(root)
frame.pack(pady=20)

block_btn = Button(frame, text="Block", command=block_websites, bg="red", fg="white", width=10)
block_btn.grid(row=0, column=0, padx=10)

unblock_btn = Button(frame, text="Unblock", command=unblock_websites, bg="green", fg="white", width=10)
unblock_btn.grid(row=0, column=1, padx=10)

exit_btn = Button(root, text="Exit", command=root.quit, width=10)
exit_btn.pack(pady=10)

root.mainloop()
