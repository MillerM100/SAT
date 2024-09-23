from customtkinter import *
import json
import time

# Set app dimensions, title, and appearance mode
app = CTk()
app.geometry("900x550")
app.title("SAT Practice Program")
set_appearance_mode("light")
start_time = None

# Create frames for different pages
main_frame = CTkFrame(master=app, fg_color="#FFFFFF")
flashcard_frame = CTkFrame(master=app, fg_color="#FFFFFF")
results_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # New results frame

# Variables to track scores
correct_count = 0
wrong_count = 0

# Function to show a specific frame
def show_frame(frame):
    global start_time, flipped
    frame.tkraise()

    if frame == main_frame:
        start_time = None
    elif frame == flashcard_frame:
        global current_card_index
        current_card_index = 0
        start_time = time.time()
        flipped = False  # Reset flipped state when entering flashcard frame
        show_flashcard()
        update_timer()

# Function to format time
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Function to update the timer label
def update_timer():
    global start_time
    if start_time is not None:
        elapsed_time = int(time.time() - start_time)
        timer_label.configure(text=format_time(elapsed_time))
        flashcard_frame.after(1000, update_timer)

# Set up and stack frames
for frame in (main_frame, flashcard_frame, results_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load flashcard content from JSON file
def clean_definition(definition):
    # Replace unwanted characters
    return definition.replace("Â", "").replace("â", "").replace("²", "²")

with open("C:\\Users\\mikah\\OneDrive\\Desktop\\Formulas100.json", 'r', encoding='utf-8') as file:
    flashcards_data = json.load(file)

# Clean the definitions in flashcards
for card in flashcards_data:
    card['definition'] = clean_definition(card['definition'])

flashcards = flashcards_data
current_card_index = 0
wrong_count = 0
flipped = False

# Create function to show the flashcard
def show_flashcard():
    global current_card_index, flipped
    card_term = flashcards[current_card_index]['term']
    card_definition = flashcards[current_card_index]['definition']

    # If flipped, show definition; if not, show term
    if flipped:
        term_label.configure(text=card_definition)
    else:
        term_label.configure(text=card_term.upper())

    # Update the flashcard number label
    flashcard_number_label.configure(text=f"{current_card_index + 1} / {len(flashcards)}")

# Function to set up the main page
def setup_main_page():
    btn_flashcard = CTkButton(master=main_frame, width=265, height=105, text="FORMULA\nFLASHCARDS",
                              font=("Helvetica", 28, "bold"), text_color="#009ADA", corner_radius=25,
                              fg_color="#ffffff", hover_color="#f5f8fc", border_color="#000000", border_width=2.2,
                              command=lambda: show_frame(flashcard_frame))
    btn_flashcard.place(relx=0.5, rely=0.8, anchor="center")

    frame = CTkFrame(master=main_frame, width=500, height=190, corner_radius=40, fg_color="white", border_width=2.15,
                     border_color="black")
    frame.place(relx=0.5, rely=0.3, anchor="center")

    label = CTkLabel(master=frame, text="SAT PRACTICE", font=("Helvetica", 55, "bold"), text_color="#009ADA")
    label.place(relx=0.5, rely=0.3, anchor="center")

    label_description = CTkLabel(master=frame, text="Prepare for Bluebook's Digital SAT Test with this free practice "
                                                    "resource. Click the FORMULA FLASHCARDS button to begin.",
                                 font=("Roboto", 18.3), text_color="#000000", wraplength=400)
    label_description.place(relx=0.5, rely=0.7, anchor="center")

# Function to set up flashcard page
def setup_flashcard_page():
    global term_label, flashcard_number_label, flipped, btn_right, btn_wrong

    btn_back = CTkButton(master=flashcard_frame, width=150, height=40, text="RETURN TO HOME",
                         font=("Helvetica", 16, "bold"),
                         text_color="#009ADA", corner_radius=8, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(main_frame))
    btn_back.place(relx=0.75, rely=0.85, anchor="center")

    # Set up frame for flashcard
    flashcard_container = CTkFrame(master=flashcard_frame, width=700, height=360, corner_radius=20, fg_color="white",
                                   border_width=2.15, border_color="black")
    flashcard_container.place(relx=0.5, rely=0.44, anchor="center")

    flashcard_number_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 24, "bold"),
                                      text_color="#009ADA")
    flashcard_number_label.place(relx=0.5, rely=0.85, anchor="center")

    timer_frame = CTkFrame(master=flashcard_frame, width=300, height=30, corner_radius=5, fg_color="white",
                           border_width=2.15, border_color="black")
    timer_frame.place(relx=0.5, rely=0.06, anchor="center")

    global timer_label
    timer_label = CTkLabel(master=timer_frame, text="00:00", font=("Helvetica", 20, "bold"), text_color="#009ADA")
    timer_label.place(relx=0.5, rely=0.5, anchor="center")

    # Create label for the flashcard term/formula
    term_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 40, "bold"), text_color="#009ADA")
    term_label.place(relx=0.5, rely=0.43, anchor="center")

    # Bind click event to toggle flashcard display (flip between term and definition)
    flashcard_container.bind("<Button-1>", lambda e: toggle_flashcard())

    # Show the first flashcard
    show_flashcard()

    # Create buttons for right/wrong feedback
    btn_correct = CTkButton(master=flashcard_frame, text="RIGHT",
                            font=("Helvetica", 12, "bold"),
                            fg_color="#ffffff", text_color="black", corner_radius=8)
    btn_correct.place(relx=0.05, rely=0.4, anchor="center")

    btn_incorrect = CTkButton(master=flashcard_frame, text="WRONG",
                              font=("Helvetica", 18, "bold"),
                              fg_color="#ffffff", text_color="black", corner_radius=8)
    btn_incorrect.place(relx=0.05, rely=0.6, anchor="center")

    canvas = CTkCanvas(master=flashcard_frame, width=870, height=3, bg="#000000", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.68, anchor="center")
    canvas.create_line(0, 1, 700, 1, fill="black", width=4)

    # Add label for the click instruction
    instruction_label = CTkLabel(master=flashcard_frame, text="CLICK THE CARD TO FLIP", font=("Helvetica", 24, "bold"),
                                 text_color="#009ADA")
    instruction_label.place(relx=0.5, rely=0.721, anchor="center")

    # Create frames for navigation buttons
    prev_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    prev_frame.place(relx=0.40, rely=0.85, anchor="center")
    next_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    next_frame.place(relx=0.60, rely=0.85, anchor="center")

    # Create navigation buttons
    btn_previous = CTkButton(prev_frame, text="←", command=lambda: change_flashcard(-1), font=("Helvetica", 40, "bold"),
                             fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2,
                             width=60, height=60)
    btn_previous.pack(expand=True)

    btn_next = CTkButton(next_frame, text="→", command=lambda: change_flashcard(1), font=("Helvetica", 40, "bold"),
                         fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2,
                         width=60, height=60)
    btn_next.pack(expand=True)

# Function to toggle flashcard display (flip between term and definition)
def toggle_flashcard():
    global flipped
    flipped = not flipped
    show_flashcard()

# Function to change flashcard based on direction
def change_flashcard(direction):
    global current_card_index
    current_card_index += direction

    # Loop back to start/end if needed
    if current_card_index < 0:
        current_card_index = len(flashcards) - 1
    elif current_card_index >= len(flashcards):
        current_card_index = 0

    flipped = False  # Reset flipped state when changing cards
    show_flashcard()

# Set up the main page and flashcard page
setup_main_page()
setup_flashcard_page()

# Show the main frame initially
show_frame(main_frame)

# Start the application
app.mainloop()
