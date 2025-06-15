import customtkinter as ctk


class Loginform(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("600x400")

        # Container to hold both frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Initialize frames
        self.login_frame = self.create_login_frame()
        self.quiz_frame = self.create_quiz_frame()

        # Start with login frame
        self.show_frame(self.login_frame)

    def create_login_frame(self):
        frame = ctk.CTkFrame(self.container)

        name_label = ctk.CTkLabel(frame, text="Enter Your Name:")
        name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.pack(pady=10)

        roll_label = ctk.CTkLabel(frame, text="Enter Your Roll Number:")
        roll_label.pack(pady=10)
        self.roll_entry = ctk.CTkEntry(frame)
        self.roll_entry.pack(pady=10)

        next_button = ctk.CTkButton(
            frame, text="Start Quiz", command=self.go_to_quiz)
        next_button.pack(pady=20)

        return frame

    def create_quiz_frame(self):
        frame = ctk.CTkFrame(self.container)

        label = ctk.CTkLabel(frame, text="Welcome to the Quiz!")
        label.pack(pady=20)

        back_button = ctk.CTkButton(
            frame, text="Back to Login", command=lambda: self.show_frame(self.login_frame))
        back_button.pack(pady=10)

        return frame

    def show_frame(self, frame):
        # Hide all frames
        for child in self.container.winfo_children():
            child.pack_forget()
        # Show the selected frame
        frame.pack(fill="both", expand=True)

    def go_to_quiz(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()

        if not name or not roll:
            ctk.CTkMessagebox(
                title="Warning", message="Please fill in all fields")
            return

        self.show_frame(self.quiz_frame)


app = Loginform()
app.mainloop()
