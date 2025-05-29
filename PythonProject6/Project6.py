import tkinter as tk
from tkinter import messagebox, mainloop
from tkinter import Label
from tkinter import *

root=tk.Tk()
root.title("Login")
root.geometry("300x200")

def login():
    username=entry1.get()
    password=entry2.get()

    if (username==""" and password="""):
        messagebox.showinfo("","Blank Not Allowed")

    elif (username=="Project" and password=="Admin"):
        messagebox.showinfo("","Login Success")

    else:
        messagebox.showinfo("","Incorrect username and password")

    print("Login button clicked")

global entry1
global entry2

Label(root,text="username").place(x=20,y=20)
Label(root,text="password").place(x=20,y=70)

entry1=Entry(root,bd=5)
entry1.place(x=140,y=20)

entry2=Entry(root,bd=5)
entry2.place(x=140,y=70)

Button(root,text="Login",command=login,height=3,width=13,bd=6).place(x=100,y=120)

root,mainloop()