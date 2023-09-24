import tkinter as tk
from tkinter import ttk
from MailHelper import MailHelper

class LoginPage(tk.Frame):
    def __init__(self, parent, switch_to_info_page):
        super().__init__(parent)
        self.parent = parent

        # Title
        title_label = ttk.Label(self, text="ParentControls.Win Login")
        title_label.pack(pady=20)

        # Login form
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.try_login)
        self.login_button.pack()

    def try_login(self):
        # perform server login, assume success
        try_login = True

        if try_login:
            switch_to_info_page()

"""
class InfoPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.info_label = tk.Label(self, text="Welcome to the information page!")
        self.info_label.pack()
"""

class InfoPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Title
        title_label = ttk.Label(self, text="Information Page")
        title_label.pack(pady=20)
        
        # Forum
        forum_label = ttk.Label(self, text="Write a Message:")
        forum_label.pack()
        
        self.message_entry = ttk.Entry(self)
        self.message_entry.pack(pady=5)
        self.message_entry.insert(0, "Add message here")
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)
        self.message_entry.bind("<FocusOut>", self.restore_placeholder)
        
        submit_button = ttk.Button(self, text="Submit", command=self.submit_message)
        submit_button.pack(pady=10)
    
        # Status label
        self.status_label = ttk.Label(self, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
    def submit_message(self):
        message = self.message_entry.get()
        
        # You can add your logic to process the submitted message here
        support_mailer = MailHelper()
        send_status = support_mailer.send_email(message)
        
        # For demonstration purposes, we'll just show a success message
        if send_status:
            self.status_label.config(text="Message sent successfully!")
        else:
            self.status_label.config(text="Message failed to send")

        support_mailer.close()

    def clear_placeholder(self, event):
        if self.message_entry.get() == "Add message here":
            self.message_entry.delete(0, tk.END)
    
    def restore_placeholder(self, event):
        if not self.message_entry.get():
            self.message_entry.insert(0, "Add message here")

def switch_to_info_page():
    login_frame.pack_forget()
    information_frame.pack()

# Create the main application window
root = tk.Tk()
root.title("App")

# Create instances of the login and information frames
login_frame = LoginPage(root, switch_to_info_page)
information_frame = InfoPage(root)

# Start with the login frame visible
login_frame.pack()

# Run the Tkinter main loop
root.mainloop()

