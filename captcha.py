import random
import string
import tkinter as tk

class Captcha:
    def __init__(self, window):
        self.window = window
        self.master = tk.Toplevel(window)
        self.master.geometry("300x150")
        self.master.title("Captcha")
        self.value = False
        
        self.label = tk.Label(self.master, text="Enter the captcha")
        self.label.pack()

        self.captcha = self.generate_captcha()
        self.captcha_label = tk.Label(self.master, text=self.captcha, font=('Courier New', 12, 'underline'), fg='orange', bg='black')
        self.captcha_label.pack()

        self.entry = tk.Entry(self.master)
        self.entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_captcha)
        self.submit_button.pack()

    def generate_captcha(self):
        captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return captcha

    def check_captcha(self):
        global value
        if self.entry.get() == self.captcha:
            self.master.destroy()
            self.value = True
        else:
            self.label.config(text="Captcha did not match. Please try again.")
            self.captcha = self.generate_captcha()
            self.captcha_label.config(text=self.captcha)
            self.entry.delete(0, tk.END)
    def answer(self):
        return self.value




