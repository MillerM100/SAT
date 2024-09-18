from customtkinter import *

app = CTk()
app.geometry("900x600")

set_appearance_mode("light")
background_frame = CTkFrame(master=app, fg_color="white")
background_frame.pack(fill="both", expand=True)

btn = CTkButton(master=app, text="Flashcards", corner_radius=10, fg_color="#ffffff",
                hover_color="#f5f8fc", border_color="#000000", border_width=2)
btn.place(relx=0.5, rely=0.5, anchor="center")

frame = CTkFrame(master=app, width=440, height=170, corner_radius=20, fg_color="transparent", border_width=2, border_color="black")
frame.place(relx=0.5, rely=0.3, anchor="center")

label = CTkLabel(master=frame, text="SAT PRACTICE", font=("Helvetica", 40, "bold"), text_color="#009ADA")
label.place(relx=0.5, rely=0.5, anchor="center")

canvas = CTkCanvas(app, width=900, height=600, bg='white', highlightthickness=0)
canvas.create_line(0, 300, 900, 300, fill="black", width=2)

app.mainloop()