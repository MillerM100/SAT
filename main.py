from customtkinter import *

# Set app dimensions and title
app = CTk()
app.geometry("900x550")
app.title("SAT Practice Program")

# Set background colour and appearance mode
background_frame = CTkFrame(master=app, fg_color="#FFFFFF")
background_frame.pack(fill="both", expand=True)
set_appearance_mode("light")

# Function to create the new page for flashcards
def open_flashcard_page():
    for widget in app.winfo_children():
        widget.destroy()

# Open new page when flashcard clicked
btn_flashcard = CTkButton(master=app, width=265, height=105, text="FORMULA\nFLASHCARDS", font=("Helvetica", 28, "bold"),
                          text_color="#009ADA", corner_radius=25, fg_color="#ffffff",
                          hover_color="#f5f8fc", border_color="#000000", border_width=2.2,
                          command=open_flashcard_page)
btn_flashcard.place(relx=0.3, rely=0.8, anchor="center")

# Add practice question button with text split into two lines
btn_practice = CTkButton(master=app, width=265, height=105, text="PRACTICE\nQUESTIONS", font=("Helvetica", 28, "bold"),
                         text_color="#009ADA", corner_radius=25, fg_color="#ffffff",
                         hover_color="#f5f8fc", border_color="#000000", border_width=2.2)
btn_practice.place(relx=0.7, rely=0.8, anchor="center")

# Add translate button
btn_translate = CTkButton(master=app, width=150, height=30, text="TRANSLATE", font=("Helvetica", 16, "bold"),
                          text_color="#009ADA", corner_radius=8, fg_color="#ffffff",
                          hover_color="#f5f8fc", border_color="#000000", border_width=2.2)
btn_translate.place(relx=0.90, rely=0.05, anchor="center")

# Create frame around heading
frame = CTkFrame(master=app, width=500, height=190, corner_radius=40, fg_color="white", border_width=2.15,
                 border_color="black")
frame.place(relx=0.5, rely=0.3, anchor="center")

# Label the frame with heading
label = CTkLabel(master=frame, text="SAT PRACTICE", font=("Helvetica", 55, "bold"), text_color="#009ADA")
label.place(relx=0.5, rely=0.3, anchor="center")

# Create horizontal line
canvas = CTkCanvas(master=app, width=2100, height=3, bg="#000000", highlightthickness=0)
canvas.place(relx=0.5, rely=0.59, anchor="center")
canvas.create_line(0, 1, 900, 1, fill="black", width=2)

# Label for description with text wrapping
label_description = CTkLabel(master=frame, text="Prepare for Bluebook's Digital SAT Test with this free practice "
                                                "resource. Select between formula flashcards or timed practice "
                                                "questions.",
                             font=("Roboto", 18.3), text_color="#000000", wraplength=400)  # Set wrap length to 400
label_description.place(relx=0.5, rely=0.7, anchor="center")

app.mainloop()
