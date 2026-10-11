import tkinter as tk
from tkinter import scrolledtext, Entry
import threading
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import wikipedia
import random
import subprocess
import os

def speak(text):
    """Function to speak out text safely by initializing engine locally to avoid thread lockups."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Female voice if available
        else:
            engine.setProperty('voice', voices[0].id)
            
        clean_text = text.replace("Aura:", "").strip()
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AURA ASSISTANT")
        self.root.geometry("500x600")
        self.root.configure(bg="#0B0F19")

        # Color Palette (Aesthetic Cyber Dark)
        self.BG_MAIN = "#0B0F19"
        self.CARD_BG = "#161F30"
        self.BORDER_CLR = "#233048"
        self.ACCENT_PRIMARY = "#6366F1"  # Indigo
        self.ACCENT_ACTIVE = "#EF4444"   # Red during recording
        self.TEXT_MAIN = "#F8FAFC"
        self.TEXT_MUTED = "#94A3B8"
        self.USER_MSG_CLR = "#38BDF8"

        # Title / Header
        title_label = tk.Label(
            root, text="AURA ASSISTANT", 
            font=("Arial", 16, "bold"), 
            bg=self.BG_MAIN, fg=self.ACCENT_PRIMARY
        )
        title_label.pack(side=tk.TOP, pady=10)

        # Status Label
        self.status_label = tk.Label(
            root, text="Status: Idle", 
            font=("Arial", 10), 
            bg=self.BG_MAIN, fg=self.TEXT_MUTED
        )
        self.status_label.pack(side=tk.BOTTOM, pady=5)

        # Frame for Input, Send Button & Speak Button
        input_frame = tk.Frame(root, bg=self.BG_MAIN)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=5)

        self.user_entry = Entry(
            input_frame, font=("Arial", 12),
            bg=self.CARD_BG, fg=self.TEXT_MAIN,
            insertbackground='white'
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_entry.bind("<Return>", lambda event: self.process_text_input())

        send_btn = tk.Button(
            input_frame, text="Send", 
            command=self.process_text_input,
            bg=self.ACCENT_PRIMARY, fg="white",
            font=("Arial", 10, "bold"), relief=tk.FLAT, padx=8
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))

        speak_btn = tk.Button(
            input_frame, text="🎙️ Speak", 
            command=self.start_listening_thread,
            bg=self.ACCENT_ACTIVE, fg="white",
            font=("Arial", 10, "bold"), relief=tk.FLAT, padx=8
        )
        speak_btn.pack(side=tk.LEFT)

        # Chat History Box
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state='disabled',
            bg=self.CARD_BG, fg=self.TEXT_MAIN,
            font=("Arial", 11), insertbackground='white'
        )
        self.chat_display.pack(side=tk.TOP, padx=15, pady=5, fill=tk.BOTH, expand=True)

        # Greet on startup
        welcome_text = "Aura: Hello! I am Aura, your assistant. You can speak or type your commands."
        self.append_chat(welcome_text)
        threading.Thread(target=lambda: speak("Hello! I am Aura, your assistant.")).start()

    def append_chat(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + "\n\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def process_text_input(self):
        text = self.user_entry.get().strip()
        if text:
            self.append_chat(f"You (Typed): {text}")
            self.user_entry.delete(0, tk.END)
            threading.Thread(target=self.handle_command, args=(text,)).start()

    def start_listening_thread(self):
        threading.Thread(target=self.listen_from_mic).start()

    def listen_from_mic(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.status_label.config(text="Status: Listening...", fg="#EF4444")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                self.status_label.config(text="Status: Processing...", fg="#F59E0B")
                query = r.recognize_google(audio, language='en-in')
                self.append_chat(f"You (Voice): {query}")
                self.status_label.config(text="Status: Idle", fg="#94A3B8")
                self.handle_command(query)
            except sr.WaitTimeoutError:
                self.status_label.config(text="Status: Idle", fg="#94A3B8")
                response = "Aura: Listening timed out. Please try again."
                self.append_chat(response)
                threading.Thread(target=lambda: speak(response)).start()
            except Exception as e:
                self.status_label.config(text="Status: Idle", fg="#94A3B8")
                response = "Aura: Sorry, I could not understand your voice."
                self.append_chat(response)
                threading.Thread(target=lambda: speak(response)).start()

    def handle_command(self, command):
        cmd = command.lower()
        
        # Time command
        if "time" in cmd:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"Aura: The current time is {current_time}"
            self.append_chat(response)
            threading.Thread(target=lambda: speak(response)).start()
            
        # Date command
        elif "date" in cmd:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Aura: Today's date is {current_date}"
            self.append_chat(response)
            threading.Thread(target=lambda: speak(response)).start()

        # Open Websites
        elif "open google" in cmd:
            response = "Aura: Opening Google for you."
            self.append_chat(response)
            webbrowser.open("https://www.google.com")
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open youtube" in cmd:
            response = "Aura: Opening YouTube for you."
            self.append_chat(response)
            webbrowser.open("https://www.youtube.com")
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open facebook" in cmd:
            response = "Aura: Opening Facebook for you."
            self.append_chat(response)
            webbrowser.open("https://www.facebook.com")
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open github" in cmd:
            response = "Aura: Opening GitHub for you."
            self.append_chat(response)
            webbrowser.open("https://www.github.com")
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open stackoverflow" in cmd:
            response = "Aura: Opening Stack Overflow for you."
            self.append_chat(response)
            webbrowser.open("https://stackoverflow.com")
            threading.Thread(target=lambda: speak(response)).start()

        # Open System Apps / Tools
        elif "open notepad" in cmd:
            response = "Aura: Opening Notepad."
            self.append_chat(response)
            subprocess.Popen(['notepad.exe'])
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open calculator" in cmd:
            response = "Aura: Opening Calculator."
            self.append_chat(response)
            subprocess.Popen(['calc.exe'])
            threading.Thread(target=lambda: speak(response)).start()
            
        elif "open cmd" in cmd or "command prompt" in cmd:
            response = "Aura: Opening Command Prompt."
            self.append_chat(response)
            subprocess.Popen(['cmd.exe'])
            threading.Thread(target=lambda: speak(response)).start()

        # Wikipedia Search
        elif "wikipedia" in cmd or "search" in cmd:
            search_msg = "Aura: Searching Wikipedia..."
            self.append_chat(search_msg)
            threading.Thread(target=lambda: speak("Searching Wikipedia")).start()
            try:
                query = cmd.replace("wikipedia", "").replace("search", "").strip()
                result = wikipedia.summary(query, sentences=2)
                response = f"Aura: {result}"
                self.append_chat(response)
                threading.Thread(target=lambda: speak(response)).start()
            except Exception as e:
                response = "Aura: Sorry, I couldn't find anything on Wikipedia."
                self.append_chat(response)
                threading.Thread(target=lambda: speak(response)).start()
                
        # Default Google Search fallback
        else:
            response = f"Aura: Searching Google for {command}."
            self.append_chat(response)
            webbrowser.open(f"https://www.google.com/search?q={command}")
            threading.Thread(target=lambda: speak(response)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()