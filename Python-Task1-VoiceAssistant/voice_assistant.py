import os
import datetime
import webbrowser
import threading
import io
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write

# --- TTS Engine Setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    update_chat(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def update_chat(message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, message + "\n\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

# --- Command Handler ---
def process_command(command):
    command = command.lower().strip()
    if not command:
        return

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open spotify" in command:
        speak("Opening spotify")
        webbrowser.open("https://www.spotify.com")
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What would you like me to search for?")
    elif "bye" in command or "exit" in command:
        speak("Goodbye! Have a great day!")
        root.destroy()
    else:
        speak(f"You said: {command}")


#--- voice recording and recognition ---

def record_and_listen():
    btn_listen.config(state=tk.DISABLED, text="Listening...")
    lbl_status.config(text="Listening... Speak clearly now!", fg="#FF5722")
    root.update()

    sample_rate = 16000  
    duration = 5        

    try:
        # Direct int16 recording to avoid conversion distortion
        raw_audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

        # Convert to WAV format in memory
        byte_io = io.BytesIO()
        write(byte_io, sample_rate, raw_audio)
        byte_io.seek(0)

        # Recognize with Google API
        recognizer = sr.Recognizer()
        with sr.AudioFile(byte_io) as source:
            audio_source = recognizer.record(source)
            text = recognizer.recognize_google(audio_source)
            update_chat(f"You: {text}")
            process_command(text)

    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said. Please try speaking a bit closer to the mic.")
    except sr.RequestError:
        speak("Network issue. Please check your internet connection.")
    except Exception as e:
        speak("Microphone error. You can also type below.")
        print(f"Error details: {e}")

    btn_listen.config(state=tk.NORMAL, text="🎤 Speak Command")
    lbl_status.config(text="Ready", fg="#4CAF50")

def start_listening_thread():
    threading.Thread(target=record_and_listen, daemon=True).start()

def send_text_command(event=None):
    cmd = entry_cmd.get().strip()
    if cmd:
        entry_cmd.delete(0, tk.END)
        update_chat(f"You: {cmd}")
        threading.Thread(target=process_command, args=(cmd,), daemon=True).start()

# --- GUI Window ---
root = tk.Tk()
root.title("OIBSIP - Voice Assistant")
root.geometry("450x530")
root.resizable(False, False)

title_lbl = tk.Label(root, text="Personal Voice Assistant", font=("Arial", 16, "bold"))
title_lbl.pack(pady=10)

lbl_status = tk.Label(root, text="Ready", font=("Arial", 10, "italic"), fg="#4CAF50")
lbl_status.pack()

# Chat Area
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=48, height=15, font=("Arial", 10))
chat_box.pack(pady=10, padx=10)
chat_box.config(state=tk.DISABLED)

# Voice Button
btn_listen = tk.Button(root, text="🎤 Speak Command", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=20, command=start_listening_thread)
btn_listen.pack(pady=6)

# Text Input Option
frame_input = tk.Frame(root)
frame_input.pack(pady=8, padx=10, fill=tk.X)

entry_cmd = tk.Entry(frame_input, font=("Arial", 10))
entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry_cmd.bind("<Return>", send_text_command)

btn_send = tk.Button(frame_input, text="Send", font=("Arial", 9, "bold"), bg="#2196F3", fg="white", command=send_text_command)
btn_send.pack(side=tk.RIGHT)

root.mainloop()