import customtkinter as ctk
from login import create_csv
import cv2
from tkinter import messagebox
from PIL import Image

app = ctk.CTk()


class Loginform(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.image_captured = False
        self.image_path = "yet_to_capture.png"

        self.title("Kurukshetra")
        self.geometry("1000X1000")

        self.title("Kurukshetra")
        self.geometry("1000x1000")
        self.grid_columnconfigure((0, 1), weight=1)

        name_label = ctk.CTkLabel(self, text="Enter Your Name :")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        roll_label = ctk.CTkLabel(self, text="Enter you roll number :")
        roll_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.roll_entry = ctk.CTkEntry(self)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ctk.CTkButton(
            self, text="Start Quiz now !!", command=self.login_button_fun)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.capture_image_button = ctk.CTkButton(
            self, text="Capture Your Photo", command=self.capture_image)
        self.capture_image_button.grid(row=2, column=0, columnspan=2, pady=20)

        image = Image.open(self.image_path)
        self.capture_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(100, 100))
        self.img_label = ctk.CTkLabel(self, image=self.capture_image, text="")
        self.img_label.grid(row=0, column=3, rowspan=3, padx=10)
        self.img_label.grid(row=0, column=3, rowspan=3, padx=10)

    def login_button_fun(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        create_csv([name, roll])

    def capture_image(self):
        self.get_image()

    def get_image(self):
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            self.alert_and_exit("Webcam not opened")

        cv2.namedWindow("test")

        while not self.image_captured:
            ret, frame = cam.read()
            if not ret:
                self.alert_and_exit("Unable to read from webcam")
                break

            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 32:  # SPACE pressed
                img_name = "opencv_frame.png"
                cv2.imwrite(img_name, frame)
                self.image_captured = False
                self.image_path = img_name
                print(f"Image saved as {img_name}")
                break

        cam.release()
        cv2.destroyAllWindows()

    def alert_and_exit(self, msg):
        messagebox.showerror(
            title="Alert", message=f"The program has experienced failure due to : {msg}")
        exit()


app = Loginform()
app.mainloop()
