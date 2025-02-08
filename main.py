import tkinter as tk
from tkinter import messagebox, simpledialog
import speech_recognition as sr
import os
import json
import threading
import datetime
import time
import requests

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice-Controlled To-Do List with AI Reminders")
        self.root.geometry("500x650")

        # Create a gradient background
        self.canvas = tk.Canvas(root, width=500, height=650)
        self.canvas.pack(fill="both", expand=True)
        self.create_gradient()

        self.tasks = []
        self.reminders = []
        self.load_data()

        # Task List
        self.task_listbox = tk.Listbox(root, width=50, height=10, bg="#4b0082", fg="white", font=("Arial", 12), selectbackground="#8a2be2")
        self.task_listbox.place(x=50, y=100)

        # Motivational Quote
        self.quote_label = tk.Label(root, text=self.get_motivational_quote(), wraplength=400, bg="#4b0082", fg="white", font=("Arial", 12, "italic"))
        self.quote_label.place(x=50, y=250)

        # Command Entry
        self.command_entry = tk.Entry(root, width=50, bg="#8a2be2", fg="white", font=("Arial", 12))
        self.command_entry.place(x=50, y=300)
        self.command_entry.bind("<Return>", self.process_text_command)

        # Start Voice Command Button
        self.start_button = tk.Button(root, text="Start Voice Command", command=self.start_voice_command_thread, bg="#ff4500", fg="white", font=("Arial", 12, "bold"), activebackground="#ff6347")
        self.start_button.place(x=150, y=350)
        self.start_button.bind("<Enter>", self.on_hover)
        self.start_button.bind("<Leave>", self.on_leave)
        
        self.recognizer = sr.Recognizer()

        self.update_task_list()
        self.check_reminders_thread()

    def create_gradient(self):
        """Creates a smooth gradient background."""
        for i in range(650):
            r = max(0, 255 - i // 2)  # Ensure value is not negative
            g = 140  # Constant green for a purple tone
            b = max(0, 255 - i // 3)  # Ensure value is not negative
            color = f"#{r:02x}{g:02x}{b:02x}"  # Convert to hex color
            self.canvas.create_line(0, i, 500, i, fill=color, width=2)

    def on_hover(self, event):
        event.widget.config(bg="#ff6347")

    def on_leave(self, event):
        event.widget.config(bg="#ff4500")

    def start_voice_command_thread(self):
        """Runs the voice command function without blocking UI."""
        self.root.after(100, self.start_voice_command)

    def start_voice_command(self):
        """Handles speech recognition and processes commands."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for commands...")
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                self.process_command(command)
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError:
                print("Could not connect to Google Speech Recognition service.")

    def process_text_command(self, event):
        """Processes text input command from the entry box."""
        command = self.command_entry.get().lower().strip()
        if command:
            print(f"You typed: {command}")
            self.process_command(command)
            self.command_entry.delete(0, tk.END)

    def process_command(self, command):
        """Processes user commands and updates task list accordingly."""
        print(f"Processing command: {command}")

        if "add" in command:
            task = command.replace("add", "").strip()
            if not task:
                print("No task detected.")
                return
            print(f"Adding task: {task}")
            self.tasks.append(task)
            self.update_task_list()
            self.save_data()
        elif "remove" in command:
            task = command.replace("remove", "").strip()
            if task in self.tasks:
                print(f"Removing task: {task}")
                self.tasks.remove(task)
                self.update_task_list()
                self.save_data()
        elif "show" in command:
            print("Showing tasks...")
            self.update_task_list()
        elif "remind me to" in command:
            self.set_reminder(command)

    def set_reminder(self, command):
        """Sets a reminder based on voice or text input."""
        try:
            parts = command.split("remind me to")
            task = parts[1].strip() if len(parts) > 1 else ""
            if task:
                reminder_time = self.ask_for_datetime()
                if reminder_time:
                    self.reminders.append({"task": task, "time": reminder_time})
                    self.save_data()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def ask_for_datetime(self):
        """Asks the user for a reminder time and returns a datetime object."""
        date_time_str = simpledialog.askstring("Set Reminder", "Enter date and time (YYYY-MM-DD HH:MM):")
        if date_time_str:
            try:
                return datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid date and time format.")
        return None

    def check_reminders_thread(self):
        """Starts a separate thread to check for reminders."""
        threading.Thread(target=self.check_reminders, daemon=True).start()

    def check_reminders(self):
        """Checks if any reminder time has passed and shows alerts."""
        while True:
            now = datetime.datetime.now()
            for reminder in self.reminders[:]:
                if reminder["time"] <= now:
                    messagebox.showinfo("Reminder", f"Reminder: {reminder['task']}")
                    self.reminders.remove(reminder)
                    self.save_data()
            time.sleep(60)

    def update_task_list(self):
        """Updates the task listbox with current tasks."""
        print("Updating task list...")
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def save_data(self):
        """Saves tasks and reminders to a JSON file."""
        with open("tasks.json", "w") as f:
            json.dump({"tasks": self.tasks, "reminders": self.reminders}, f, default=str)

    def load_data(self):
        """Loads tasks and reminders from a JSON file if it exists."""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                try:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.reminders = data.get("reminders", [])
                except json.JSONDecodeError:
                    self.tasks = []
                    self.reminders = []
                    print("Warning: tasks.json is corrupted. Resetting tasks and reminders.")

    def get_motivational_quote(self):
        """Fetches a motivational quote from an API."""
        try:
            response = requests.get("https://api.quotable.io/random")
            if response.status_code == 200:
                return response.json().get("content", "Stay positive and work hard!")
        except requests.RequestException:
            pass
        return "Stay positive and work hard!"

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
