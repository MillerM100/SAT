import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk

if __name__ == '__main__':

    # Create the main GUI window
    root = tk.Tk()
    root.title('Flashcards App')
    root.geometry('1000x680')
    root.configure(bg='white')

    # Load the image as an icon
    icon_image = PhotoImage(file=r"C:\Users\mikah\OneDrive\Pictures\SAT ICON.png")
    root.iconphoto(True, icon_image)

    # Apply styling to the GUI elements
    style = Style(theme='superhero')
    style.configure('TLabel', font=('TkDefault', 18))
    style.configure('TButton', font=('TkDefault', 16))

    # Set up variables for storing user input
    set_name_var = tk.StringVar()
    word_var = tk.StringVar()
    definition_var = tk.StringVar()

    # Create a notebook widget to manage tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    root.mainloop()
