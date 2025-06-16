import customtkinter as ctk
from login import create_csv
import cv2
from tkinter import messagebox
from PIL import Image
from get_questions import get_data
import time
import matplotlib.pyplot as plt


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.image_captured = False
        self.image_path = "yet_to_capture.png"

        self.question = ""
        self.options = ""
        self.correct_answer = []

        self.selected_options = []

        self.chart_colors = ["#74ff00", "#ff3200"]
        self.chart_labels = ["Correct Answers", "Wrong Answers"]

        self.name = ""
        self.roll_number = ""

        # Initialize results_frame as None
        self.results_frame = None

        self.title("Kurukshetra")
        self.geometry("1000x1000")
        self.grid_columnconfigure((0, 1), weight=1)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.login_frame = self.create_login_frame()
        self.show_frame(self.login_frame)

    def create_login_frame(self):
        frame = ctk.CTkFrame(self.container)

        name_label = ctk.CTkLabel(frame, text="Enter Your Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        roll_label = ctk.CTkLabel(frame, text="Enter your Roll Number:")
        roll_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.roll_entry = ctk.CTkEntry(frame)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=10)

        self.capture_image_button = ctk.CTkButton(
            frame, text="Capture Your Photo", command=self.capture_image)
        self.capture_image_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.login_button = ctk.CTkButton(
            frame, text="Start Quiz Now!!", command=self.login_button_fun)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        image = Image.open(self.image_path)
        self.capture_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(100, 100))
        self.img_label = ctk.CTkLabel(frame, image=self.capture_image, text="")
        self.img_label.grid(row=0, column=3, rowspan=3, padx=10)

        return frame

    def login_button_fun(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        if not name or not roll:
            messagebox.showwarning("Missing Info", "Please fill in the blanks")
            return
        create_csv([name, roll])
        self.name = name
        self.roll_number = roll
        self.show_frame(self.quiz_frame())
        self.start_time = time.time()
        self.update_timer()

    def quiz_frame(self):
        quizframe = ctk.CTkFrame(self.container)
        quizframe.grid_columnconfigure(0, weight=0)
        quizframe.grid_columnconfigure(1, weight=1)
        quizframe.grid_rowconfigure(0, weight=1)

        # Sidebar setup
        self.sidebar = ctk.CTkFrame(quizframe, corner_radius=1)
        self.sidebar.grid(row=0, column=0, sticky='nsw')

        try:
            self.sidebar_image = Image.open("opencv_frame.png")
            self.sidebar_image_ctk = ctk.CTkImage(
                self.sidebar_image, size=(100, 100))
            self.sidebar_image_label = ctk.CTkLabel(
                self.sidebar, image=self.sidebar_image_ctk, text="")
        except:
            self.sidebar_image_label = ctk.CTkLabel(
                self.sidebar, text="Profile Pic")
        self.sidebar_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_sidebar_label = ctk.CTkLabel(self.sidebar, text=self.name)
        self.name_sidebar_label.grid(row=1, column=0, padx=10, pady=10)

        self.roll_sidebar_label = ctk.CTkLabel(
            self.sidebar, text=self.roll_number)
        self.roll_sidebar_label.grid(row=2, column=0, padx=10, pady=10)

        self.timer_label = ctk.CTkLabel(
            self.sidebar, text="00:00:00", font=("Arial", 16))
        self.timer_label.grid(row=3, column=0, padx=10, pady=10)

        # Quiz area setup
        self.quiz_area = ctk.CTkScrollableFrame(quizframe)
        self.quiz_area.grid(row=0, column=1, sticky="nsew")
        self.quiz_area.grid_columnconfigure(0, weight=1)

        # Clear previous selections
        self.selected_options = []

        # Create questions
        for i in range(1, 6):
            self.get_questions(id=i)

            question_container = ctk.CTkFrame(self.quiz_area)
            question_container.pack(fill="x", pady=10, padx=10)

            question_label = ctk.CTkLabel(
                question_container, text=f"Q{i}: {self.question}", anchor="w")
            question_label.pack(anchor="w", pady=(0, 5))

            # Single StringVar per question
            option_var = ctk.StringVar(value="")
            self.selected_options.append(option_var)  # Store for submission

            # Create radio buttons sharing the same variable
            for option in self.options:
                radio = ctk.CTkRadioButton(
                    question_container,
                    text=option,
                    variable=option_var,
                    value=option
                )
                radio.pack(anchor="w", pady=2)

        self.submit_button = ctk.CTkButton(
            self.quiz_area, text="Submit Answers", command=self.submit_answers)
        self.submit_button.pack(pady=20)

        return quizframe

    def create_results_frame(self):
        frame = ctk.CTkFrame(self.container)

        name_label = ctk.CTkLabel(frame, text=f"Name: {self.name}")
        name_label.grid(row=0, column=0, sticky='nsw', padx=20, pady=10)

        roll_label = ctk.CTkLabel(
            frame, text=f"Roll Number: {self.roll_number}")
        roll_label.grid(row=1, column=0, sticky='nsw', padx=20, pady=10)

        try:
            profile_image = Image.open("opencv_frame.png")
            profile_image_ctk = ctk.CTkImage(profile_image, size=(100, 100))
            image_label = ctk.CTkLabel(frame, image=profile_image_ctk, text="")
            image_label.grid(row=0, column=1, rowspan=2, padx=20, pady=10)
        except FileNotFoundError:
            image_label = ctk.CTkLabel(frame, text="No Profile Image")
            image_label.grid(row=0, column=1, rowspan=2, padx=20, pady=10)

        try:
            result_chart = Image.open("Result.png")
            chart_image_ctk = ctk.CTkImage(result_chart, size=(300, 300))
            chart_label = ctk.CTkLabel(frame, image=chart_image_ctk, text="")
            chart_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        except FileNotFoundError:
            chart_label = ctk.CTkLabel(frame, text="Results Not Available")
            chart_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        return frame

    def submit_answers(self):
        no_answers_correct = 0
        data = get_data()

        answers = []

        for i, option_var in enumerate(self.selected_options):
            self.selected_options.append(option_var)

        print(self.selected_options)

        for i in range(1, 6):
            answers.append(data[str(i)]['correct_answer'])
        for i in range(5):
            if answers[i] == self.selected_options[i]:
                print(answers[i])
                print(self.selected_options[i].get())
                no_answers_correct += 1
        wrong_answers = 5 - no_answers_correct
        chart_value = [no_answers_correct, wrong_answers]

        plt.figure(figsize=(6, 6))
        plt.pie(chart_value, labels=self.chart_labels,
                autopct='%1.1f%%', startangle=90, colors=self.chart_colors)
        plt.title("Results")
        plt.savefig("Result.png")
        plt.close()

        self.results_frame = self.create_results_frame()
        self.show_frame(self.results_frame)

    def get_questions(self, id):
        data = get_data()  # get_data() takes no parameters
        self.question = data[str(id)]["question"]
        self.options = data[str(id)]["options"]

    def capture_image(self):
        messagebox.showinfo("Info", "Press Space bar to capture your image")
        self.get_image()
        self.image_captured = False

    def show_frame(self, frame):
        for child in self.container.winfo_children():
            child.pack_forget()
        frame.pack(fill="both", expand=True)

    def get_image(self):
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            self.alert_and_exit("Webcam not opened")

        cv2.namedWindow("Capture Image")
        while not self.image_captured:
            ret, frame = cam.read()
            if not ret:
                self.alert_and_exit("Unable to read from webcam")
                break

            cv2.imshow("Capture Image", frame)
            k = cv2.waitKey(1)
            if k % 256 == 32:  # SPACE pressed
                img_name = "opencv_frame.png"
                cv2.imwrite(img_name, frame)
                self.image_captured = True
                self.image_path = img_name
                break

        cam.release()
        cv2.destroyAllWindows()

        image = Image.open(self.image_path)
        self.capture_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(100, 100))
        self.img_label.configure(image=self.capture_image)

    def alert_and_exit(self, msg):
        messagebox.showerror(
            title="Alert", message=f"The program has experienced failure due to: {msg}")
        exit()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        if hasattr(self, 'timer_label'):
            self.timer_label.configure(
                text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.after(1000, self.update_timer)


app = GUI()
app.mainloop()
