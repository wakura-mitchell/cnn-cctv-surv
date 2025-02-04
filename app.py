import threading
import time
import customtkinter as ctk
import tkinter.messagebox as tkmb
import tkinter as tk

# Selecting GUI theme - dark, light, system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")


class LoginApp:
    def login(self, app):
        self.app = app
        self.app.geometry('400x500')
        self.app.title("Smart City Surveillance System")
        self.loginFrame()

    def loginFrame(self):
        label = ctk.CTkLabel(self.app, text="Secure Login System")
        label.pack(pady=20)

        frame = ctk.CTkFrame(self.app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(frame, text='Please login to continue')
        label.pack(pady=12)

        self.username = ctk.CTkEntry(frame, placeholder_text="Username", width=220, height=50)
        self.username.pack(pady=12)

        self.password = ctk.CTkEntry(frame, placeholder_text="Password", width=220, height=50, show="*")
        self.password.pack(pady=12)

        button = ctk.CTkButton(frame, text='Login', width=250, height=50, command=self.checkCredentials)
        button.pack(pady=12)

        checkbox = ctk.CTkCheckBox(frame, text='Remember Me')
        checkbox.pack(pady=12)

    def checkCredentials(self):
        username = self.username.get()
        password = self.password.get()

        if username == "smart" and password == "city":
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully")
            self.login_success()
        elif username == "smart" and password != "city":
            tkmb.showwarning(title='Wrong password', message='Please check your password')
        elif username != "smart" and password == "city":
            tkmb.showwarning(title='Wrong username', message='Please check your username')
        else:
            tkmb.showerror(title="Login Failed", message="Invalid username and password")

    def login_success(self):
        self.app.withdraw()

        loading_window = ctk.CTk()
        loading_window.geometry("300x200")
        loading_window.title("Loading")

        loading_label = ctk.CTkLabel(loading_window, text="Loading model and initializing camera...")
        loading_label.pack(pady=20)

        progress_bar = tk.ttk.Progressbar(loading_window, length=200, mode="indeterminate")
        progress_bar.pack(pady=10)

        thread = threading.Thread(target=self.run_video_classification, args=(progress_bar,))
        thread.start()

        while thread.is_alive():
            progress_bar.step(10)
            loading_window.update()
            time.sleep(0.5)

        loading_window.destroy()
        self.app.deiconify()

    def run_video_classification(self, progress_bar):
        # Perform the necessary operations in VideoClassification
        from videoClassification import VideoClassification
        VideoClassification()
        progress_bar.stop()