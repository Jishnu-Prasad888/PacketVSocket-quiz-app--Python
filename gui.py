import customtkinter as ctk
from login import create_csv
import cv2
from tkinter import messagebox
from PIL import Image
from get_questions import get_data
import time


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.image_captured = False
        self.image_path = "yet_to_capture.png"

        self.question = ""
        self.options = ""
        self.correctanser = ""

        self.selected_options = []

        self.name = ""
        self.roll_number = ""

        self.title("Kurukshetra")
        self.geometry("1000x1000")
        self.grid_columnconfigure((0, 1), weight=1)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.login_frame = self.create_login_frame()
        self.show_frame(self.login_frame)

    def create_login_frame(self):
        frame = ctk.CTkFrame(self.container)

        name_label = ctk.CTkLabel(frame, text="Enter Your Name :")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        roll_label = ctk.CTkLabel(frame, text="Enter you roll number :")
        roll_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.roll_entry = ctk.CTkEntry(frame)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ctk.CTkButton(
            frame, text="Start Quiz now !!", command=self.login_button_fun)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.capture_image_button = ctk.CTkButton(
            frame, text="Capture Your Photo", command=self.capture_image)
        self.capture_image_button.grid(
            row=2, column=0, columnspan=2, pady=20)

        image = Image.open(self.image_path)
        self.capture_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(100, 100))
        self.img_label = ctk.CTkLabel(
            frame, image=self.capture_image, text="")
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

        # -------------- Sidebar ----------

        # sidebar doesnt stretch horizontally
        quizframe.grid_columnconfigure(0, weight=0)
        # main area stretches horizontally
        quizframe.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(quizframe, corner_radius=1)
        self.sidebar.grid(row=0, column=0, sticky='nsw')

        self.sidebar_image = Image.open("opencv_frame.png")
        self.sidebar_image_label = ctk.CTkLabel(
            self.sidebar, text="Profile Pic")
        self.sidebar_image_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_sidebar_label = ctk.CTkLabel(
            self.sidebar, text=self.name)
        self.name_sidebar_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="n")

        self.roll_sidebar_label = ctk.CTkLabel(
            self.sidebar, text=self.roll_number)
        self.roll_sidebar_label.grid(
            row=2, column=0, padx=10, pady=10, sticky="n")

        self.timer_label = ctk.CTkLabel(
            self.sidebar, text="00:00:00", font=("Arial", 16))
        self.timer_label.grid(row=3, column=0, padx=10, pady=10)

        # ---------------main content ---------

        self.quiz_area = ctk.CTkScrollableFrame(quizframe,)
        self.quiz_area.grid(column=1, sticky="nsew")
        self.quiz_area.grid_rowconfigure(0, weight=1)
        self.quiz_area.grid_columnconfigure(1, weight=1)

        for i in range(1, 6):
            self.get_questions(id=i)

            self.question_frame = ctk.CTkScrollableFrame(quizframe,)
            self.question_frame.grid(row=i, column=1, sticky="nsew")
            selected_option = ctk.StringVar(value="")
            question = ctk.CTkLabel(
                self.question_frame, text=self.question, anchor="w")
            radio1 = ctk.CTkRadioButton(
                self.question_frame, text=self.options[0], variable=selected_option, value=self.options[0])
            radio2 = ctk.CTkRadioButton(
                self.question_frame, text=self.options[1], variable=selected_option, value=self.options[1])
            radio3 = ctk.CTkRadioButton(
                self.question_frame, text=self.options[2], variable=selected_option, value=self.options[2])
            radio4 = ctk.CTkRadioButton(
                self.question_frame, text=self.options[3], variable=selected_option, value=self.options[3])
            self.selected_options.append(selected_option)
            question.pack(pady=10)
            radio1.pack(anchor="w", pady=5)
            radio2.pack(anchor="w", pady=5)
            radio3.pack(anchor="w", pady=5)
            radio4.pack(anchor="w", pady=5)
        return quizframe

    def get_questions(self, id):
        data = get_data()
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

        cv2.namedWindow("Capture Window")

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
                print(f"Image saved as {img_name}")
                break
        cam.release()
        cv2.destroyAllWindows()

        self.image = Image.open(self.image_path)
        self.capture_image = ctk.CTkImage(
            light_image=self.image, dark_image=self.image, size=(100, 100))
        self.img_label.configure(image=self.capture_image)

    def alert_and_exit(self, msg):
        messagebox.showerror(
            title="Alert", message=f"The program has experienced failure due to : {msg}")
        exit()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        if hasattr(self, 'timer_label'):  # only update if timer exists
            self.timer_label.configure(
                text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.after(1000, self.update_timer)


app = GUI()
app.mainloop()
