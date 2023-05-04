import tkinter as tk
import sqlite3
import hashlib
import re
import random
import string
from email_sender import EmailSender
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
from io import BytesIO


connection = sqlite3.connect("userdata.db")
cur = connection.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS userdata(
                id INTEGER PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
            """)
root = tk.Tk()
root.title("Menu")
root.attributes('-fullscreen', True)
root.configure(bg="#ffffff")

username_register = None
password_register = None
email_register = None
status_label_register = None
username_login = None
password_login = None
status_label_login = None
login_window = None

button_style = {'font': ('Arial', 14), 'fg': 'white', 'bg': 'blue', 'width': 10, 'height': 1, 'bd': 0}

email_sender = EmailSender('angelvalkovback@gmail.com', 'kbieocfvcojxnhju')


def register_window():
    
    global username_register, password_register, email_register, status_label_register
    registerWindow = tk.Toplevel(root)
    registerWindow.title("Register")
    registerWindow.geometry("500x300")
    registerWindow.resizable(False, False)
    registerWindow.configure(bg="#ffffff")

    username_label = tk.Label(registerWindow, text="Username:", font=("Helvetica", 12), bg="#f5f5f5")
    username_label.place(x=50, y=50)
    username_register = tk.Entry(registerWindow, font=("Helvetica", 12))
    username_register.place(x=200, y=50, width=200)

    password_label = tk.Label(registerWindow, text="Password:", font=("Helvetica", 12), bg="#f5f5f5")
    password_label.place(x=50, y=100)
    password_register = tk.Entry(registerWindow, show="*", font=("Helvetica", 12))
    password_register.place(x=200, y=100, width=200)

    email_label = tk.Label(registerWindow, text="Email:", font=("Helvetica", 12), bg="#f5f5f5")
    email_label.place(x=50, y=150)
    email_register = tk.Entry(registerWindow, font=("Helvetica", 12))
    email_register.place(x=200, y=150, width=200)

    register_button = tk.Button(registerWindow, text="Register", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=register_user)
    register_button.place(x=200, y=220)

    status_label_register = tk.Label(registerWindow, text="", font=("Helvetica", 12), bg="#f5f5f5")
    status_label_register.place(x=200, y=250)

    
def validate_account(username, password, email, label):
        if len(username)>6:
            if re.search(r'\d', password) and re.search(r'[a-zA-Z]', password) and len(password)>8:
                if len(email)>8 and email.count("@")>0:
                    
                    
                    return True
                    
                else:
                    label.config(text="emails must contain '@' and more than 8 symbols")
            else:
                label.config(text="Password must contain a letter and a digit and be more that 8 symbols")
        else:
            label.config(text="The username must be more that 6 symbols")
def register_user():
    global username_register, password_register, email_register
    username = username_register.get()
    password = password_register.get()
    email = email_register.get()
    
    cur.execute("SELECT id FROM userdata WHERE username=?", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        status_label_register.config(text="Username already taken")
        return
    
    if validate_account(username, password, email, status_label_register):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO userdata (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        connection.commit()
        status_label_register.config(text="User registered successfully")
        subject = 'Account Created'
        body = f'Hi, {username}. You created an account in our software!'
        email_sender.send_email(email, subject, body)


def login_window():
    
    global username_login, password_login, status_label_login
    loginWindow = tk.Toplevel(root)
    loginWindow.title("Login")
    loginWindow.geometry("500x300")
    loginWindow.resizable(False, False)
    loginWindow.configure(bg="#ffffff")
    loginWindow.bind('<Escape>', lambda e: loginWindow.destroy())

   
    frame = tk.Frame(loginWindow)

    
    username_label = tk.Label(frame, text="Username:", font=("Arial", 14))
    username_label.grid(row=0, column=0, padx=20, pady=10)
    username_login = tk.Entry(frame, font=("Arial", 14))
    username_login.grid(row=0, column=1, padx=20, pady=10)

    
    password_label = tk.Label(frame, text="Password:", font=("Arial", 14))
    password_label.grid(row=1, column=0, padx=20, pady=10)
    password_login = tk.Entry(frame, show="*", font=("Arial", 14))
    password_login.grid(row=1, column=1, padx=20, pady=10)

    
    login_button = tk.Button(frame, text="Login", command=login_user, font=("Arial", 14), bg="blue", fg="white", width=10)
    login_button.grid(row=2, column=0, padx=20, pady=10)

    
    forgot_password_button = tk.Button(frame, text="Forgotten password", command=forgot_password, font=("Arial", 14), bg="orange", fg="white", width=20)
    forgot_password_button.grid(row=2, column=1, padx=20, pady=10)

    
    status_label_login = tk.Label(frame, text="", font=("Arial", 14))
    status_label_login.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

    frame.pack()

def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=8))
    return password
    
def forgot_password():
    global username_login
    usernameLogin = username_login.get()
    new_password = generate_password()
    hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
    cur.execute("SELECT * FROM userdata WHERE username=?", (usernameLogin,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("UPDATE userdata SET password=? WHERE id=?", (hashed_new_password, user_id))
        connection.commit()
        email = user[3]
        subject = "Forgotten password"
        body = f'This is your new password: {new_password}'
        email_sender.send_email(email, subject, body) 
    else:
        status_label_login.config(text="Can't create your new password")
    
def login_user():
    global username_login, password_login
    usernameLogin = username_login.get()
    passwordLogin = password_login.get()
    hashed_passwordLogin = hashlib.sha256(passwordLogin.encode()).hexdigest()
    
    cur.execute("SELECT * FROM userdata WHERE username=? AND password=?", (usernameLogin, hashed_passwordLogin))
    user = cur.fetchone()
    
    if user:
        status_label_login.config(text="Login successful")
        accountWindow = tk.Toplevel(root)
        accountWindow.title("Account Options")
        accountWindow.geometry("500x300")
        accountWindow.resizable(False, False)
        accountWindow.configure(bg="#ffffff")
        accountWindow.bind('<Escape>', lambda e: accountWindow.destroy())

        status_label_account = tk.Label(accountWindow, text='Hi, '+str(usernameLogin), font=("Arial", 30), bg="white")
        status_label_account.pack(pady=20)

        update_button = tk.Button(accountWindow, text="Update Account", command=update_window, font=("Arial", 14), bg="orange", fg="white", width=20, height=2)
        update_button.pack(pady=10)

        delete_button = tk.Button(accountWindow, text="Delete Account", command=delete_account, font=("Arial", 14), bg="orange", fg="white", width=20, height=2)
        delete_button.pack(pady=10)
        
    else:
        status_label_login.config(text="Invalid username or password")

def update_window():
    global username_login, password_login, status_label_update
    username = username_login.get()
    
    cur.execute("SELECT * FROM userdata WHERE username=?", (username,))
    user = cur.fetchone()
    
    if user:
        updateWindow = tk.Toplevel(root)
        updateWindow.title("Update Account")
        updateWindow.geometry("500x300")
        updateWindow.configure(bg="#ffffff")
        updateWindow.resizable(False, False)
        updateWindow.bind('<Escape>', lambda e: updateWindow.destroy())

        username_label = tk.Label(updateWindow, text="Current Username: " + user[1], bg="#ffffff")
        username_label.place(x=50, y=50)
        username_new_label = tk.Label(updateWindow, text="New Username:", bg="#ffffff")
        username_new_label.place(x=50, y=80)
        username_new_entry = tk.Entry(updateWindow)
        username_new_entry.place(x=200, y=80, width=200)

        password_label = tk.Label(updateWindow, text="Current Password: " + "*" * 8, bg="#ffffff")
        password_label.place(x=50, y=120)
        password_new_label = tk.Label(updateWindow, text="New Password:", bg="#ffffff")
        password_new_label.place(x=50, y=150)
        password_new_entry = tk.Entry(updateWindow, show="*", bg="#ffffff")
        password_new_entry.place(x=200, y=150, width=200)

        email_label = tk.Label(updateWindow, text="Current Email: " + user[3], bg="#ffffff")
        email_label.place(x=50, y=190)
        email_new_label = tk.Label(updateWindow, text="New Email:", bg="#ffffff")
        email_new_label.place(x=50, y=220)
        email_new_entry = tk.Entry(updateWindow)
        email_new_entry.place(x=200, y=220, width=200)

        update_button = tk.Button(updateWindow, text="Update", command=lambda: update_user(user[0], username_new_entry.get(), password_new_entry.get(), email_new_entry.get()), bg="green")
        update_button.place(x=200, y=270, width=100, height=40)

        status_label_update = tk.Label(updateWindow, text="", bg="#ffffff")
        status_label_update.place(x=200, y=250)

    else:
        status_label_update.config(text="Invalid account to update")

def update_user(user_id, new_username, new_password, new_email):
    global username_login, status_label_update
    if validate_account(new_username, new_password, new_email, status_label_update):
        cur.execute("SELECT id FROM userdata WHERE username=?", (new_username,))
        row = cur.fetchone()
        if row and row[0] != user_id:
            status_label_update.config(text="Username already taken")
            return
        if new_username:
            cur.execute("UPDATE userdata SET username=? WHERE id=?", (new_username, user_id))
            username_login.delete(0, 'end')
            username_login.insert(0, new_username)
        if new_password:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cur.execute("UPDATE userdata SET password=? WHERE id=?", (hashed_password, user_id))
        if new_email:
            cur.execute("UPDATE userdata SET email=? WHERE id=?", (new_email, user_id))
    
        connection.commit()
        status_label_update.config(text="User updated successfully")

def delete_account():
    global username_login, password_login
    username = username_login.get()
    password = password_login.get()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("SELECT * FROM userdata WHERE username=? AND password=?", (username, hashed_password))
    user = cur.fetchone()

    if user:
        cur.execute("DELETE FROM userdata WHERE username=? AND password=?", (username, hashed_password))
        connection.commit()
        status_label_account.config(text="Account deleted successfully")
        username_login.delete(0, 'end')
        password_login.delete(0, 'end')
    else:
        status_label_account.config(text="Invalid username or password")
        



login_button_menu = tk.Button(root, text="Login", command=login_window, **button_style)
login_button_menu.pack(pady=10)

register_button_menu = tk.Button(root, text="Register", command=register_window, **button_style)
register_button_menu.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy, **button_style)
exit_button.pack(pady=10)

root.mainloop()
