from customtkinter import *
import json
import time
import random

# Set app dimensions, title, and appearance mode
app = CTk()
app.geometry("900x550")
app.title("SAT Practice Program")
set_appearance_mode("light")
start_time = None
elapsed_time = 0
numCorrect = 0
numWrong = 0
numFlashcards = 0

# Create frames for different pages
main_frame = CTkFrame(master=app, fg_color="#FFFFFF")
flashcard_frame = CTkFrame(master=app, fg_color="#FFFFFF")
results_frame = CTkFrame(master=app, fg_color="#FFFFFF")
end_frame = CTkFrame(master=app, fg_color="#FFFFFF")

def show_flashcard(is_correct):
    global numFlashcards, numCorrect
    numFlashcards += 1

    if is_correct:
        numCorrect += 1

# Function to show a specific frame
def show_frame(frame):
    global start_time, flipped, end_time
    frame.tkraise()

    if frame == main_frame:
        start_time = None
    elif frame == flashcard_frame:
        global current_card_index
        current_card_index = 0
        start_time = time.time()
        flipped = False
        random.shuffle(flashcards)
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
for frame in (main_frame, flashcard_frame, results_frame, end_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def answer_correct():
    global numCorrect, numFlashcards
    numCorrect += 1
    numFlashcards += 1
    print(f"Answer Correct: {numCorrect} correct, {numFlashcards} total")

def answer_incorrect():
    global numFlashcards
    numFlashcards += 1
    print(f"Answer Incorrect: {numCorrect} correct, {numFlashcards} total")

# Load flashcard content from JSON file
def clean_definition(definition):
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

# Create the end_session function
def end_session():
    global elapsed_time
    elapsed_time = int(time.time() - start_time)
    show_frame(end_frame)
    display_results()

# Create function to show the flashcard
def show_flashcard():
    global current_card_index, flipped
    card_term = flashcards[current_card_index]['term']
    card_definition = flashcards[current_card_index]['definition']

    if flipped:
        term_label.configure(text=card_definition)
    else:
        term_label.configure(text=card_term.upper())

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

    line_canvas = CTkCanvas(master=main_frame, width=1800, height=3, bg="#000000", highlightthickness=0)
    line_canvas.place(relx=0.5, rely=0.6, anchor="center")

# Function to set up flashcard page
def setup_flashcard_page():
    global term_label, flashcard_number_label, flipped, btn_right, btn_wrong

    btn_back = CTkButton(master=flashcard_frame, width=150, height=40, text="RETURN TO HOME",
                         font=("Helvetica", 16, "bold"),
                         text_color="#009ADA", corner_radius=8, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(main_frame))
    btn_back.place(relx=0.75, rely=0.85, anchor="center")

    btn_end = CTkButton(master=flashcard_frame, width=150, height=40, text="END SESSION",
                        font=("Helvetica", 16, "bold"),
                        text_color="#009ADA", corner_radius=8, fg_color="#ffffff", hover_color="#f5f8fc",
                        border_color="#000000", border_width=2.2,
                        command=lambda: end_session())
    btn_end.place(relx=0.25, rely=0.85, anchor="center")

    flashcard_container = CTkFrame(master=flashcard_frame, width=700, height=360, corner_radius=20, fg_color="white",
                                   border_width=2.15, border_color="black")
    flashcard_container.place(relx=0.5, rely=0.44, anchor="center")

    # Define hover color change functions
    def on_enter(event):
        flashcard_container.configure(fg_color="#f5f8fc")

    def on_leave(event):
        flashcard_container.configure(fg_color="white")

    # Bind the events
    flashcard_container.bind("<Enter>", on_enter)
    flashcard_container.bind("<Leave>", on_leave)

    flashcard_number_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 24, "bold"),
                                      text_color="#009ADA")
    flashcard_number_label.place(relx=0.5, rely=0.85, anchor="center")

    timer_frame = CTkFrame(master=flashcard_frame, width=300, height=30, corner_radius=5, fg_color="white",
                           border_width=2.15, border_color="black")
    timer_frame.place(relx=0.5, rely=0.06, anchor="center")

    global timer_label
    timer_label = CTkLabel(master=timer_frame, text="00:00", font=("Helvetica", 20, "bold"), text_color="#009ADA")
    timer_label.place(relx=0.5, rely=0.5, anchor="center")

    term_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 40, "bold"), text_color="#009ADA")
    term_label.place(relx=0.5, rely=0.43, anchor="center")

    flashcard_container.bind("<Button-1>", lambda e: toggle_flashcard())

    show_flashcard()

    btn_correct = CTkButton(master=flashcard_frame, text="CORRECT", command=lambda: handle_answer(True),
                            font=("Helvetica", 20, "bold"),
                            fg_color="#e8ffd6", text_color="#009ADA", corner_radius=8,
                            border_color="#000000", border_width=2.2, hover_color="#b9eba4")
    btn_correct.place(relx=0.22, rely=0.06, anchor="center")

    btn_incorrect = CTkButton(master=flashcard_frame, text="INCORRECT", command=lambda: handle_answer(False),
                              font=("Helvetica", 20, "bold"),
                              fg_color="#ffd8d6", text_color="#009ADA", corner_radius=8,
                              border_color="#000000", border_width=2.2, hover_color="#ffb7b5")
    btn_incorrect.place(relx=0.78, rely=0.06, anchor="center")

    canvas = CTkCanvas(master=flashcard_frame, width=870, height=3, bg="#000000", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.68, anchor="center")
    canvas.create_line(0, 1, 700, 1, fill="black", width=4)

    instruction_label = CTkLabel(master=flashcard_frame, text="CLICK THE CARD TO FLIP", font=("Helvetica", 24, "bold"),
                                 text_color="#009ADA")
    instruction_label.place(relx=0.5, rely=0.721, anchor="center")

    prev_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    prev_frame.place(relx=0.40, rely=0.85, anchor="center")
    next_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    next_frame.place(relx=0.60, rely=0.85, anchor="center")

    btn_previous = CTkButton(prev_frame, text="←", command=lambda: change_flashcard(-1), font=("Helvetica", 40, "bold"),
                             fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2.2,
                             width=60, height=58, hover_color="#f5f8fc")
    btn_previous.pack(expand=True)

    btn_next = CTkButton(next_frame, text="→", command=lambda: change_flashcard(1), font=("Helvetica", 40, "bold"),
                         fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2.2,
                         width=60, height=58, hover_color="#f5f8fc")
    btn_next.pack(expand=True)

def handle_answer(is_correct):
    global numCorrect, numWrong, current_card_index, flipped
    if is_correct:
        numCorrect += 1
    else:
        numWrong += 1

    current_card_index += 1
    if current_card_index < len(flashcards):
        flipped = False
        show_flashcard()
    else:
        end_session()

def setup_end_page():
    global correct_label

    line_canvas = CTkCanvas(master=end_frame, width=1800, height=3, bg="#000000", highlightthickness=0)
    line_canvas.place(relx=0.5, rely=0.6, anchor="center")

    btn_home = CTkButton(master=end_frame, width=265, height=95, text="RETURN TO HOME",
                         font=("Helvetica", 28, "bold"),
                         text_color="#009ADA", corner_radius=25, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(main_frame))
    btn_home.place(relx=0.78, rely=0.8, anchor="center")

    btn_home = CTkButton(master=end_frame, width=265, height=95, text="TRY AGAIN",
                         font=("Helvetica", 28, "bold"),
                         text_color="#009ADA", corner_radius=25, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(flashcard_frame))
    btn_home.place(relx=0.22, rely=0.8, anchor="center")

    frame = CTkFrame(master=end_frame, width=600, height=190, corner_radius=40, fg_color="white", border_width=2.15,
                     border_color="black")
    frame.place(relx=0.5, rely=0.25, anchor="center")

    label = CTkLabel(master=frame, text="KEEP PRACTICING", font=("Helvetica", 55, "bold"), text_color="#009ADA")
    label.place(relx=0.5, rely=0.3, anchor="center")

def toggle_flashcard():
    global flipped
    flipped = not flipped
    show_flashcard()

def end_flashcards():
    setup_end_page()

def change_flashcard(direction):
    global current_card_index, flipped

    if direction == 1:
        current_card_index += 1
    elif direction == -1:
        current_card_index -= 1

    # Ensure current_card_index stays within bounds
    if current_card_index < 0:
        current_card_index = 0
    elif current_card_index >= len(flashcards):
        current_card_index = len(flashcards) - 1

    flipped = False 
    show_flashcard()

setup_main_page()
setup_flashcard_page()
setup_end_page()

def display_results():
    global correct_label, wrong_label

    # Add elapsed time display below the correct_label
    time_label = CTkLabel(master=end_frame, text=f"{format_time(elapsed_time)} SECONDS TAKEN", font=("Helvetica", 22, "bold"),
                          text_color="#000")
    time_label.place(relx=0.637, rely=0.315, anchor="center")

    results_label = CTkLabel(master=end_frame, text=f"{numCorrect}/{numWrong+numCorrect} CORRECT",
                          font=("Helvetica", 22, "bold"),
                          text_color="#000")
    results_label.place(relx=0.302, rely=0.315, anchor="center")

show_frame(main_frame)

# Start the app
app.mainloop()