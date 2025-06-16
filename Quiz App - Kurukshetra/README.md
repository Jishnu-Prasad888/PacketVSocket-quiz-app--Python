# PacketVSocket-quiz-app--Python
# Kurukshetra - Facial Authenticated Quiz Application

_A desktop-based quiz app with webcam authentication, built using `customtkinter`, OpenCV, and matplotlib._

---

## 🚀 Features

- Facial image capture for quiz entry
- Real-time timer during quiz
- Scrollable quiz interface with radio button options
- Result pie chart generation with correct/wrong answer breakdown
- Saves student info to CSV

---

## 🛠️ Technologies Used

- **Python**
- **CustomTkinter** – Modern UI framework for tkinter
- **OpenCV** – For capturing webcam images
- **Pillow (PIL)** – Image handling
- **matplotlib** – For generating the results chart

---

## 🧠 How It Works

1. **User enters Name & Roll Number**
2. **Captures webcam photo** for authentication
3. **Takes a quiz** with 5 questions fetched from a `get_data()` source
4. **Answers are evaluated**, and results are visualized in a pie chart
5. **Results page** shows user info, profile image, and the score chart

---

## 📂 Project Structure
project/
│
├── main.py # Main GUI logic
├── login.py # CSV writing logic
├── get_questions.py # get_data() method providing quiz questions
├── opencv_frame.png # User's captured image
├── Result.png # Pie chart image
├── yet_to_capture.png # Placeholder image before webcam capture
└── requirements.txt # Dependencies

## ▶️ How to Run

- Clone the repository:

```bash git clone https://github.com/yourusername/kurukshetra-quiz.git ```

- Install the dependencies:

```bash pip install -r requirements.txt```
- Run the app:

```bash python main.py```

## ✅ TODO / Improvements
- Add multi-user result storage

- Enable question shuffling

- Store scores with timestamps

- Facial recognition for identity (instead of just image capture)
