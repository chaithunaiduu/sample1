import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import hashlib

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Application")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        self.signin_button = tk.Button(self.frame, text="Sign In", command=self.open_signin)
        self.signin_button.grid(row=0, column=0, padx=10, pady=10)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.open_signup)
        self.signup_button.grid(row=0, column=1, padx=10, pady=10)

    def open_signin(self):
        self.new_window = tk.Toplevel(self.master)
        SignInPage(self.new_window)

    def open_signup(self):
        self.new_window = tk.Toplevel(self.master)
        SignUpPage(self.new_window)

class SignInPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Sign In")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Admin Login", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.check_credentials)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            with open("user_credentials.txt", "r") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(",")
                    if username == stored_username and hashed_password == stored_password:
                        self.master.destroy()  # Close the sign-in window
                        self.open_assessment_app()
                        return
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No user credentials found. Please sign up first.")

    def open_assessment_app(self):
        root = tk.Tk()
        app = PrakrutiAssessment(root)
        root.mainloop()

class SignUpPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Up")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Sign Up", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.signup_button = tk.Button(self.frame, text="Sign Up", command=self.save_credentials)
        self.signup_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def save_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username and password:
            with open("user_credentials.txt", "a") as file:
                file.write(f"{username},{hashed_password}\n")
            messagebox.showinfo("Success", "Account created successfully. You can now sign in.")
            self.master.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter both username and password.")

class PrakrutiAssessment:
    def __init__(self, master):
        self.master = master
        self.master.title("Prakruti Assessment")

        self.canvas = tk.Canvas(self.master)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.answers = [0] * 4  

        self.questions = [
            "Gender:",
            "Age:",
            "Any allergies?",
            "Dietary preference:",
            "How would you describe your body build:",
            "How do you respond to changes in weather:",
            "How is your appetite:",
            "How is your digestion:",
            "How do you handle stress:",
            "What is your sleep pattern like:",
            "How do you feel in the morning after waking up:",
            "How is your skin type:",
            "Do you easily gain or lose weight:",
            "What is your level of physical activity:",
            "How do you handle conflicts:",
            "How do you prefer to relax:",
            "What type of environment do you feel most comfortable in:",
            "Preferable weather:",
            "Do you smoke or drink?"
        ]

        self.choices = [
            ["Male", "Female", "Other", "Prefer not to say"],
            ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100", "100+"],
            ["None", "Pollen", "Dust", "Food", "Pet dander", "Medications"],
            ["Vegetarian", "Non-vegetarian", "Vegan", "Flexitarian"],
            ["Thin and light", "Medium", "Large and sturdy", "Athletic", "Obese"],
            ["Sensitive, gets cold easily", "Moderate", "Can tolerate extremes well", "No effect"],
            ["Variable, sometimes strong, sometimes weak", "Strong, consistent", "Irregular, often weak", "No effect"],
            ["Fast, sometimes unpredictable", "Steady", "Slow, but consistent", "No effect"],
            ["Anxious, restless", "Calm, composed", "Withdrawn, avoids confrontation", "No effect"],
            ["Regular and sound", "Variable, light sleeper", "Deep, heavy sleeper", "Insomniac"],
            ["Lethargic", "Fresh and energetic", "No effect"],
            ["Dry", "Oily", "Normal", "Combination"],
            ["Difficult to gain, easy to lose", "Moderate", "Easy to gain, difficult to lose", "No effect"],
            ["Sedentary", "Moderate", "Active", "Highly active"],
            ["Avoids conflicts", "Addresses conflicts directly", "Avoids, but feels resentment", "No effect"],
            ["Meditation/Yoga", "Physical exercise", "Spending time in nature", "Watching TV", "Reading"],
            ["Quiet and peaceful", "Dynamic and active", "Cozy and comforting", "Vibrant and bustling", "No preference"],
            ["Hot and sunny", "Cool and breezy", "Cold and snowy", "Mild and rainy"],
            ["Yes", "No"]
        ]

        self.create_widgets()

    def create_widgets(self):
        self.entries = []
        for i, question in enumerate(self.questions):
            label = tk.Label(self.scrollable_frame, text=question, font=("Helvetica", 12))
            label.grid(row=i * 5, column=0, padx=10, pady=5, sticky="w")

            var = tk.StringVar()
            self.entries.append(var)
            for j, choice in enumerate(self.choices[i]):
                tk.Radiobutton(self.scrollable_frame, text=choice, variable=var, value=str(j), font=("Helvetica", 10)).grid(row=i * 5 + j, column=1, padx=10, pady=5, sticky="w")

        self.submit_button = tk.Button(self.scrollable_frame, text="Submit", command=self.calculate_results, font=("Helvetica", 12, "bold"))
        self.submit_button.grid(row=len(self.questions) * 5, column=0, columnspan=2, pady=10)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def calculate_results(self):
        scores = [0, 0, 0, 0]
        for i, entry in enumerate(self.entries):
            answer = int(entry.get()) if entry.get().isdigit() else -1
            if answer != -1:
                if i in [0, 2, 3, 7, 9, 12, 14]:  
                    scores[0] += answer
                elif i in [1, 4, 5, 8, 11, 15, 16]:  
                    scores[1] += answer
                elif i in [6, 10, 13, 17, 18]:  
                    scores[2] += answer
                scores[3] += answer  

        max_score = max(scores)
        dominant_prakruti = ["Vata", "Pitta", "Kapha", "Tridoshic"][scores.index(max_score)]
        result_message = f"Your dominant Prakruti is: {dominant_prakruti}\n\nScores:\nVata: {scores[0]}\nPitta: {scores[1]}\nKapha: {scores[2]}\nTridoshic: {scores[3]}"

        messagebox.showinfo("Prakruti Assessment Result", result_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
