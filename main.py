import sys
import os
from customtkinter import CTk
from app import LoginApp

root = CTk()
app = LoginApp()
app.login(root)
root.mainloop()