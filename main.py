import json
import random
import time
import customtkinter as ctk
from customtkinter import *
from PIL import Image, ImageTk

# Set up window dimensions, title, appearance mode and icon
app = CTk()
app.geometry("900x550")
app.title("SAT Practice Program")
set_appearance_mode("light")
app.iconbitmap("C:\\Users\\mikah\\Downloads\\UploadImageForSAT.ico")

# Initialize tracking variables for time, correct/incorrect answers, and flashcards
start_time = None  # Track when the session begins
elapsed_time = 0  # Track the time passed in the session
numCorrect = 0  # Number of correct answers
numIncorrect = 0  # Number of incorrect answers
numFlashcards = 0  # Total number of flashcards shown

# Create frames for different sections/pages to display content separately
main_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # Main page
flashcard_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # Flashcards page
results_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # Results page
end_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # End session page
instructions_frame = CTkFrame(master=app, fg_color="#FFFFFF")  # Instructions page

# Increment flashcard count and handle correct answers
def show_flashcard(is_correct):
    global numFlashcards, numCorrect
    numFlashcards += 1  # Increase the count of flashcards shown
    print(f"Showing flashcard number: {numFlashcards}")  # Print the current flashcard number
    if is_correct:
        numCorrect += 1  # Increment answer count
        print(f"Correct answer registered. Total correct: {numCorrect}")  # Print if the answer was correct

# Function to raise the specific frame
def show_frame(frame):
    global start_time, flipped, end_time
    frame.tkraise()
    if frame == main_frame:
        start_time = None  # Show the selected frame
    elif frame == flashcard_frame:
        global current_card_index
        current_card_index = 0  # Reset flashcard index at the start
        start_time = time.time()  # Start timing
        flipped = False  # Flashcard isn't flipped initially
        random.shuffle(flashcards)  # Randomize flashcards for the session
        show_flashcard()  # Display first flashcard
        update_timer()  # Start the timer


def format_time(seconds):
    minutes = seconds // 60  # Calculate minutes
    seconds = seconds % 60  # Calculate remaining seconds
    return f"{minutes:02}:{seconds:02}"


# Function to update the timer label on the flashcard page
def update_timer():
    global start_time
    if start_time is not None:
        elapsed_time = int(time.time() - start_time)  # Calculate elapsed time
        timer_label.configure(text=format_time(elapsed_time))  # Update timer label
        flashcard_frame.after(1000, update_timer)  # Call this function again after 1 second


# Set up and stack all frames/pages to overlay one another
for frame in (main_frame, flashcard_frame, results_frame, end_frame, instructions_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)


# Function to handle correct answers
def answer_correct():
    global numCorrect, numFlashcards
    numCorrect += 1  # Increment correct answers count
    numFlashcards += 1  # Increment total flashcards count
    print(f"Answer Correct: {numCorrect} correct, {numFlashcards} total")


# Function to handle incorrect answers
def answer_incorrect():
    global numFlashcards
    numFlashcards += 1  # Increment total flashcards count
    print(f"Answer Incorrect: {numCorrect} correct, {numFlashcards} total")

# Load flashcards from a JSON file
with open("C:\\Users\\mikah\\OneDrive\\Desktop\\Formulas100.json", 'r', encoding='utf-8') as file:
    flashcards_data = json.load(file)

# Function to clean flashcard definitions by removing special characters
def clean_definition(definition):
    return definition.replace("Â", "").replace("â", "").replace("²", "²")

# Remove special characters from flashcard definitions
for card in flashcards_data:
    card['definition'] = clean_definition(card['definition'])

# Store flashcards and initialize the index for the current flashcard
flashcards = flashcards_data
current_card_index = 0  # Tracks which flashcard is currently displayed
wrong_count = 0  # Tracks number of wrong answers
flipped = False  # Tracks if the flashcard is flipped

# Function to end the session and show results
def end_session():
    global elapsed_time
    elapsed_time = int(time.time() - start_time)  # Calculate total elapsed time
    show_frame(end_frame)  # Show end session frame
    display_results()  # Display results after the session ends


# Create function to show the flashcard
def show_flashcard():
    global current_card_index, flipped
    card_term = flashcards[current_card_index]['term']  # Get current card term
    card_definition = flashcards[current_card_index]['definition']  # Get current card definition
    if flipped:
        term_label.configure(text=card_definition)  # Show definition if flipped
    else:
        term_label.configure(text=card_term.upper())  # Show term if not flipped
    flashcard_number_label.configure(text=f"{current_card_index + 1} / {len(flashcards)}")  # Display card count


# Function to set up the instructions page
def setup_instructions_page():
    # Frame for page instructions label
    guide_frame = CTkFrame(master=instructions_frame, width=850, height=500, corner_radius=40, fg_color="white",
                           border_width=2.15, border_color="black")
    guide_frame.place(relx=0.5, rely=0.3, anchor="center")

    # Label for instructions with wrapping
    instructions_label = CTkLabel(master=guide_frame,
                                   text="Welcome to the SAT practice program. After you return to the home page, "
                                        "click on the FORMULA FLASHCARDS button to begin. Click each "
                                        "flashcard to flip to the definition. Click the CORRECT "
                                        "or WRONG buttons at the top to confirm your score. "
                                        "When you are ready to move to the next flashcard, "
                                        "click the arrow buttons at the bottom of the page. "
                                        "You can move forwards and backwards between "
                                        "flashcard questions. Take note of the timer at the "
                                        "top - this can be used to manage time. When you are "
                                        "done practicing, click the END SESSION button. Your "
                                        "score will be displayed, alongside the time taken. "
                                        "From there, you can try again or head back to the home "
                                        "page. Good luck!",
                                   font=("roboto", 21), anchor="w", text_color="#000000", wraplength=750,
                                   justify="left")
    instructions_label.pack(pady=20, padx=20, fill="both", expand=True)

    # Button for returning to the home page
    btn_back_home = CTkButton(master=instructions_frame, width=265, height=105, text="RETURN TO HOME",
                              font=("Helvetica", 28, "bold"), text_color="#009ADA", corner_radius=25,
                              fg_color="#ffffff", hover_color="#f5f8fc", border_color="#000000", border_width=2.2,
                              command=lambda: show_frame(main_frame))
    btn_back_home.place(relx=0.5, rely=0.8, anchor="center")

    # Divider line canvas
    line_canvas = CTkCanvas(master=instructions_frame, width=1800, height=3, bg="#000000", highlightthickness=0)
    line_canvas.place(relx=0.5, rely=0.6, anchor="center")


# Function to set up the main page
def setup_main_page():
    # Button to start flashcards practice
    btn_flashcard = CTkButton(master=main_frame, width=265, height=105, text="FORMULA\nFLASHCARDS",
                              font=("Helvetica", 28, "bold"), text_color="#009ADA", corner_radius=25,
                              fg_color="#ffffff", hover_color="#f5f8fc", border_color="#000000", border_width=2.2,
                              command=lambda: show_frame(flashcard_frame))  # Change to show instructions
    btn_flashcard.place(relx=0.7, rely=0.8, anchor="center")

    # Button to open instructions page
    btn_info = CTkButton(master=main_frame, width=265, height=105, text="INFORMATION",
                         font=("Helvetica", 28, "bold"), text_color="#009ADA", corner_radius=25,
                         fg_color="#ffffff", hover_color="#f5f8fc", border_color="#000000", border_width=2.2,
                         command=lambda: show_frame(instructions_frame))  # Change to show instructions
    btn_info.place(relx=0.3, rely=0.8, anchor="center")

    # Frame for SAT Practice title and description
    frame = CTkFrame(master=main_frame, width=500, height=190, corner_radius=40, fg_color="white", border_width=2.15,
                     border_color="black")
    frame.place(relx=0.5, rely=0.3, anchor="center")

    # Main page label for SAT Practice
    label = CTkLabel(master=frame, text="SAT PRACTICE", font=("Helvetica", 55, "bold"), text_color="#009ADA")
    label.place(relx=0.5, rely=0.3, anchor="center")

    # Description label for the main page
    label_description = CTkLabel(master=frame, text="Prepare for Bluebook's Digital SAT Test with this free practice "
                                                    "resource. Click the FORMULA FLASHCARDS button to begin.",
                                 font=("Roboto", 18.3), text_color="#000000", wraplength=400)
    label_description.place(relx=0.5, rely=0.7, anchor="center")

    # Divider line canvas
    line_canvas = CTkCanvas(master=main_frame, width=1800, height=3, bg="#000000", highlightthickness=0)
    line_canvas.place(relx=0.5, rely=0.6, anchor="center")


# Function to set up the flashcard page
def setup_flashcard_page():
    global term_label, flashcard_number_label, flipped, btn_right, btn_wrong

    # Button to return to the main page
    btn_back = CTkButton(master=flashcard_frame, width=150, height=40, text="RETURN TO HOME",
                         font=("Helvetica", 16, "bold"),
                         text_color="#009ADA", corner_radius=8, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(main_frame))
    btn_back.place(relx=0.75, rely=0.85, anchor="center")

    # Button to end the session
    btn_end = CTkButton(master=flashcard_frame, width=150, height=40, text="END SESSION",
                        font=("Helvetica", 16, "bold"),
                        text_color="#009ADA", corner_radius=8, fg_color="#ffffff", hover_color="#f5f8fc",
                        border_color="#000000", border_width=2.2,
                        command=lambda: end_session())
    btn_end.place(relx=0.25, rely=0.85, anchor="center")

    # Flashcard container setup
    flashcard_container = CTkFrame(master=flashcard_frame, width=700, height=360, corner_radius=20, fg_color="white",
                                   border_width=2.15, border_color="black")
    flashcard_container.place(relx=0.5, rely=0.44, anchor="center")

    # Define hover color change functions for flashcard container
    def on_enter(event):
        flashcard_container.configure(fg_color="#f5f8fc")

    def on_leave(event):
        flashcard_container.configure(fg_color="white")

    # Bind the hover events
    flashcard_container.bind("<Enter>", on_enter)
    flashcard_container.bind("<Leave>", on_leave)

    # Label to show current flashcard number
    flashcard_number_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 24, "bold"),
                                      text_color="#009ADA")
    # Position the flashcard number at the bottom center of the flashcard frame
    flashcard_number_label.place(relx=0.5, rely=0.85, anchor="center")

    # Create a frame for the timer display
    timer_frame = CTkFrame(master=flashcard_frame, width=300, height=34, corner_radius=5, fg_color="white",
                           border_width=2.15, border_color="black")
    # Position the timer frame at the top center of the flashcard frame
    timer_frame.place(relx=0.5, rely=0.06, anchor="center")

    global timer_label
    # Create and position the timer label with initial time set to "00:00"
    timer_label = CTkLabel(master=timer_frame, text="00:00", font=("Helvetica", 20, "bold"), text_color="#009ADA")
    timer_label.place(relx=0.5, rely=0.47, anchor="center")

    # Create and position the term label for displaying the flashcard term
    term_label = CTkLabel(master=flashcard_frame, text="", font=("Helvetica", 40, "bold"), text_color="#009ADA")
    term_label.place(relx=0.5, rely=0.43, anchor="center")

    # Bind a click event to the flashcard container to toggle the flashcard
    flashcard_container.bind("<Button-1>", lambda e: toggle_flashcard())

    # Show the first flashcard
    show_flashcard()

    # Button for indicating a correct answer
    btn_correct = CTkButton(master=flashcard_frame, text="CORRECT", command=lambda: handle_answer(True),
                            font=("Helvetica", 20, "bold"),
                            fg_color="#e8ffd6", text_color="#009ADA", corner_radius=8,
                            border_color="#000000", border_width=2.2, hover_color="#b9eba4")
    btn_correct.place(relx=0.22, rely=0.06, anchor="center")

    # Button for indicating an incorrect answer
    btn_incorrect = CTkButton(master=flashcard_frame, text="INCORRECT", command=lambda: handle_answer(False),
                              font=("Helvetica", 20, "bold"),
                              fg_color="#ffd8d6", text_color="#009ADA", corner_radius=8,
                              border_color="#000000", border_width=2.2, hover_color="#ffb7b5")
    btn_incorrect.place(relx=0.78, rely=0.06, anchor="center")

    # Create a canvas for a horizontal line separator
    canvas = CTkCanvas(master=flashcard_frame, width=870, height=3, bg="#000000", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.68, anchor="center")
    canvas.create_line(0, 1, 700, 1, fill="black", width=4)

    # Instruction label for user guidance on how to flip the card
    instruction_label = CTkLabel(master=flashcard_frame, text="CLICK THE CARD TO FLIP", font=("Helvetica", 24, "bold"),
                                 text_color="#009ADA")
    instruction_label.place(relx=0.5, rely=0.721, anchor="center")

    # Create frames for the previous and next buttons
    prev_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    prev_frame.place(relx=0.40, rely=0.85, anchor="center")
    next_frame = CTkFrame(master=flashcard_frame, width=100, height=50)
    next_frame.place(relx=0.60, rely=0.85, anchor="center")

    # Button for navigating to the previous flashcard
    btn_previous = CTkButton(prev_frame, text="←", command=lambda: change_flashcard(-1), font=("Helvetica", 40, "bold"),
                             fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2.2,
                             width=60, height=58, hover_color="#f5f8fc")
    btn_previous.pack(expand=True)

    # Button for navigating to the next flashcard
    btn_next = CTkButton(next_frame, text="→", command=lambda: change_flashcard(1), font=("Helvetica", 40, "bold"),
                         fg_color="#ffffff", text_color="#009ADA", border_color="#000000", border_width=2.2,
                         width=60, height=58, hover_color="#f5f8fc")
    btn_next.pack(expand=True)


# Function to handle the user's answer and update the scores
def handle_answer(is_correct):
    global numCorrect, numIncorrect, current_card_index, flipped
    # Increment the correct or wrong answer count based on user input
    if is_correct:
        numCorrect += 1
    else:
        numIncorrect += 1

    # Move to the next flashcard
    current_card_index += 1
    # Show the next flashcard if available; otherwise, end the session
    if current_card_index < len(flashcards):
        flipped = False
        show_flashcard()
    else:
        end_session()


# Function to set up the end page for the flashcard session
def setup_end_page():
    global correct_label

    # Create a canvas for a line separator on the end page
    line_canvas = CTkCanvas(master=end_frame, width=1800, height=3, bg="#000000", highlightthickness=0)
    line_canvas.place(relx=0.5, rely=0.6, anchor="center")

    # Button to return to the main menu from the end page
    btn_home = CTkButton(master=end_frame, width=265, height=95, text="RETURN TO HOME",
                         font=("Helvetica", 28, "bold"),
                         text_color="#009ADA", corner_radius=25, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(main_frame))
    btn_home.place(relx=0.78, rely=0.8, anchor="center")

    # Button to retry the flashcard session from the end page
    btn_home = CTkButton(master=end_frame, width=265, height=95, text="TRY AGAIN",
                         font=("Helvetica", 28, "bold"),
                         text_color="#009ADA", corner_radius=25, fg_color="#ffffff", hover_color="#f5f8fc",
                         border_color="#000000", border_width=2.2, command=lambda: show_frame(flashcard_frame))
    btn_home.place(relx=0.22, rely=0.8, anchor="center")

    # Create a frame for the end message
    frame = CTkFrame(master=end_frame, width=600, height=190, corner_radius=40, fg_color="white", border_width=2.15,
                     border_color="black")
    frame.place(relx=0.5, rely=0.25, anchor="center")

    # Label for encouraging the user to keep practicing
    label = CTkLabel(master=frame, text="KEEP PRACTICING", font=("Helvetica", 55, "bold"), text_color="#009ADA")
    label.place(relx=0.5, rely=0.3, anchor="center")


# Flip the flashcard to show either the term or the definition based on the current state
def toggle_flashcard():
    global flipped
    flipped = not flipped  # Toggle the flipped state
    show_flashcard()  # Update the display to show the correct side


# Function to finalize the flashcard session and set up the end page
def end_flashcards():
    setup_end_page()


# Function to change the currently displayed flashcard based on the user's navigation
def change_flashcard(direction):
    global current_card_index, flipped

    # Update the current card index based on the direction (next or previous)
    if direction == 1:
        current_card_index += 1
    elif direction == -1:
        current_card_index -= 1

    # Ensure current_card_index stays within bounds
    if current_card_index < 0:
        current_card_index = 0
    elif current_card_index >= len(flashcards):
        current_card_index = len(flashcards) - 1

    flipped = False  # Reset flipped state
    show_flashcard()  # Show the updated flashcard


# Function to display final results after the session
def display_results():
    global correct_label, wrong_label

    # Add elapsed time display below the correct_label
    time_label = CTkLabel(master=end_frame, text=f"{format_time(elapsed_time)} SECONDS TAKEN",
                          font=("Helvetica", 22, "bold"),
                          text_color="#000")
    time_label.place(relx=0.637, rely=0.315, anchor="center")

    # Display the score of correct answers out of total attempts
    results_label = CTkLabel(master=end_frame, text=f"{numCorrect}/{numIncorrect + numCorrect} CORRECT",
                             font=("Helvetica", 22, "bold"),
                             text_color="#000")
    results_label.place(relx=0.302, rely=0.315, anchor="center")


# Initialize the three pages
setup_main_page()
setup_flashcard_page()
setup_end_page()
setup_instructions_page()

# Show the main frame when the program is started
show_frame(main_frame)

# Run the app
app.mainloop()

