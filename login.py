import threading
import time
from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, Frame
import customtkinter as ctk
from tkinter import ttk
from ttkthemes import ThemedTk

class LoginApp:
        
    def __init__(self, root):
        
        self.root = ThemedTk(theme="black")  # Set the theme to black
        self.root.title('Smart City Surveillance System')
        ctk.set_appearance_mode("dark")
        
        #window size
        window_width = 500
        window_height = 400
        
        #getting actual screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        #centering the window
        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.username = StringVar()
        self.password = StringVar()

        self.login_frame = self.create_login_frame()
        
    def create_login_frame(self):
        frame = ctk.CTkFrame(self.root, bg_color="blue")
        
         # Styling the labels
        self.username= ctk.CTkEntry(master=frame,placeholder_text="Username")
        self.username.pack(pady=12,padx=10)
  
        self.password= ctk.CTkEntry(master=frame,placeholder_text="Password",show="*")
        self.password.pack(pady=12,padx=10)
        
        button = ctk.CTkButton(master=frame,text='Login',command = self.check_credentials)
        button.pack(pady=12,padx=10 )
        frame.pack(pady = 50)
        return frame


    def check_credentials(self):
        if self.username.get() == 'admin' and self.password.get() == 'password':
            self.login_success()
        else:
            self.login_failure()

    def login_success(self):
        
        self.app.withdraw()

        loading_window = ctk.CTk()
        loading_window.geometry("300x200")
        loading_window.title("Loading")

        loading_label = ctk.CTkLabel(loading_window, text="Loading model and initializing camera...")
        loading_label.pack(pady=20)

        progress_bar = ctk.CTkProgressbar(loading_window, length=200, mode="indeterminate")
        progress_bar.pack(pady=10)

        thread = threading.Thread(target=self.run_video_classification, args=(progress_bar,))
        thread.start()

        while thread.is_alive():
            progress_bar.step(10)
            loading_window.update()
            time.sleep(0.5)

        loading_window.destroy()
        self.app.deiconify()
        
        self.login_frame.pack_forget()
        from videoClassification import VideoClassification
        VideoClassification()
        progress_bar.destroy()
        

    def login_failure(self):
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        Label(self.login_frame, text='Login failed. Try again.', fg='red').grid(row=4, column=2)