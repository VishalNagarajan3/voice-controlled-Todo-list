# Voice Command-Based To-Do List Application 🗣️✅

This is a Python-based voice-controlled to-do list application. Users can add, delete, or view tasks through voice commands using `speech_recognition`, and the app responds via `pyttsx3`. The application also allows task deletion via text-based prompts using `InquirerPy`.

## Features
- **Voice Commands**: Control the app by speaking commands such as "Add task," "Delete task," "View tasks," or "Exit."
- **Voice Feedback**: The app speaks back to the user to confirm actions using `pyttsx3`.
- **Text-based Deletion**: A prompt allows you to delete tasks using the command line.
- **Task Management**: Add, view, and delete tasks easily with voice interaction.

## Requirements

Make sure you have Python installed, then install the following dependencies:

```bash
pip install pyttsx3 speechrecognition InquirerPy
```

# Usage

Once the app is running, you can control the to-do list with these voice commands:

- **Add task**: The app will ask for a task, and you can speak it out.
- **Delete task**: Choose a task from the displayed list to delete.
- **View tasks**: It will speak and display all your current tasks.
- **Exit**: Closes the application.

# Example

Here’s an example of how it works:

- **You say**: "Add task"
- **App responds**: "What task would you like to add?"
- **You say**: "Buy groceries"
- **App responds**: "Task added: Buy groceries"

# Technologies Used

- **Python**: Main programming language.
- **speech_recognition**: To process voice commands.
- **pyttsx3**: For text-to-speech feedback.
- **InquirerPy**: For command line prompts (text-based interaction).
