import math
from tkinter import PhotoImage

import constants
import tkinter

class Start:
    window = None
    window_timer = None
    canvas = None
    canvas_text = None
    starter_text_label = None
    timer_text = None

    start_button = None
    reset_button = None
    check_marks = None
    current_check_marks_count = 0

    current_state = 0

    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        self.window = tkinter.Tk()
        self.window.title(constants.WINDOW_TITLE)
        self.window.config(background=constants.YELLOW, padx=100, pady=50)
        # self.window.minsize(width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT)
        # self.window.maxsize(width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT)

        self.starter_text_label = tkinter.Label(text="Timer", fg=constants.GREEN , background=constants.YELLOW, font=(constants.FONT_NAME, constants.FONT_SIZE, "bold"))
        self.starter_text_label.grid(row=0, column=1)

        self.canvas = tkinter.Canvas(width=200, height=224, background=constants.YELLOW, highlightthickness=0)
        tomato_img = PhotoImage(file="images/tomato.png")
        self.canvas.create_image(100, 112, image=tomato_img)
        self.canvas.grid(row=1, column=1)
        self.canvas_text = self.canvas.create_text(105, 130, text="00:00", fill="white", font=(constants.FONT_NAME, constants.FONT_SIZE, "bold"))

        self.start_button = tkinter.Button(text=constants.START_BUTTON_TEXT, width= 10,command=self.start_button_controller, highlightthickness=0)
        self.start_button.grid(row=2, column=0)
        self.reset_button = tkinter.Button(text=constants.RESET_BUTTON_TEXT, width= 10, command=self.reset_button_controller, highlightthickness=0)
        self.reset_button.grid(row=2, column=2)

        self.check_marks = tkinter.Label(text="here", fg=constants.GREEN, background=constants.YELLOW, font=(constants.FONT_NAME, constants.FONT_SIZE, "bold"))
        self.check_marks.grid(row=3, column=1)

        self.window.mainloop()

    def start_button_controller(self):
        print("Start button clicked")
        self.reset_timer()
        self.start_timer()

    def reset_button_controller(self):
        print("Reset button clicked")
        self.reset_timer()

    def reset_timer(self):
        self.starter_text_label.config(text="Timer", fg=constants.GREEN)
        self.canvas.itemconfig(self.canvas_text, text="00:00")
        if self.window_timer:
            self.window.after_cancel(self.window_timer)
        self.current_state = 0
        self.current_check_marks_count = 0
        self.update_check_marks()

    def start_timer(self):
        self.current_state += 1
        if self.current_state == 8:
            self.starter_text_label.config(text="Long Break", fg=constants.RED)
            self.current_check_marks_count += 1
            self.update_check_marks()
            self.start_count_down(constants.LONG_BREAK)
        elif self.current_state % 2 == 0 and self.current_state < 8:
            self.starter_text_label.config(text="Break", fg=constants.RED)
            self.current_check_marks_count += 1
            self.update_check_marks()
            self.start_count_down(constants.SHORT_BREAK)
        elif self.current_state % 2 == 1 and self.current_state < 8:
            self.starter_text_label.config(text="Work", fg=constants.GREEN)
            self.start_count_down(constants.WORK_TIME)
        else:
            self.current_state = 0
            self.current_check_marks_count = 0
            self.update_check_marks()
            self.start_timer()

    def start_count_down(self, count):
        minutes, seconds = math.floor(count / 60), count % 60
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
        self.canvas.itemconfig(self.canvas_text, text=f"{minutes}:{seconds}")
        if count == 0:
            self.start_timer()
            return
        self.window_timer = self.window.after(1000, self.start_count_down, count-1)

    def update_check_marks(self):
        check_mark_string = ""
        for num_check_marks in range(self.current_check_marks_count):
            check_mark_string += constants.CHECK_MARK
        self.check_marks.config(text=check_mark_string)