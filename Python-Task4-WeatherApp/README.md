import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import wikipedia

# Theme Palette (Aesthetic Cosmic Slate)
BG_MAIN = "#0B0F19"
CARD_BG = "#161F30"
ACCENT = "#6366F1"
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aura • AI Voice Assistant")
        self.root.geometry("450x640")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_MAIN)

        # Initialize TTS Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)
        voices = self.engine.getProperty("voices")
        if len(voices) > 1:
            self.engine.setProperty("voice", voices[1].id)  # Female voice if available

        self.is_listening = False
        self.setup_ui()
        self.speak_async("Hello! I am Aura, your voice assistant. Click the microphone or say a command.")

    def setup_ui(self):
        # Header Bar
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=(20, 10), padx=20)

        tk.Label(
            header,
            text="AURA ASSISTANT",
            font=("Montserrat", 13, "bold"),
            fg=TEXT_MAIN,
            bg=BG_MAIN
        ).pack(anchor="w")

        # Chat / Transcript Box
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            relief="flat",
            bd=0,
            padx=12,
            pady=12,
            height=18
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=10)
        self.chat_display.config(state="disabled")

        # Status & Action Container
        control_frame = tk.Frame(self.root, bg=BG_MAIN)
        control_frame.pack(fill="x", pady=15, padx=20)

        self.status_lbl = tk.Label(
            control_frame,
            text="Status: Idle",
            font=("Helvetica", 10),
            bg=BG_MAIN,
            fg=TEXT_MUTED
        )
        self.status_lbl.pack(pady=4)

        # Mic Trigger Button
        self.btn_mic = tk.Button(
            control_frame,
            text="🎙️ Tap to Speak",
            command=self.start_listening_thread,
            font=("Helvetica", 11, "bold"),
            bg=ACCENT,
            fg=TEXT_MAIN,
            activebackground="#4F46E5",
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10
        )
        self.btn_mic.pack(pady=6)

    def log(self, sender, message):
        self.chat_display.config(state="normal")
        color_tag = "user" if sender == "You" else "bot"
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n", color_tag)
        self.chat_display.tag_config("user", foreground="#38BDF8")
        self.chat_display.tag_config("bot", foreground=TEXT_MAIN)
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")

    def speak(self, text):
        self.log("Aura", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def speak_async(self, text):
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    def start_listening_thread(self):
        if not self.is_listening:
            threading.Thread(target=self.listen_and_respond, daemon=True).start()

    def listen_and_respond(self):
        self.is_listening = True
        self.status_lbl.config(text="Status: Listening...", fg="#38BDF8")
        self.btn_mic.config(bg="#EF4444", text="Listening...")

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                self.status_lbl.config(text="Status: Processing...", fg=ACCENT)
                command = recognizer.recognize_google(audio).lower()
                self.log("You", command)
                self.process_command(command)
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything.")
            except sr.UnknownValueError:
                self.speak("Sorry, I could not understand the audio.")
            except Exception as e:
                self.speak("Network or audio service error.")

        self.status_lbl.config(text="Status: Idle", fg=TEXT_MUTED)
        self.btn_mic.config(bg=ACCENT, text="🎙️ Tap to Speak")
        self.is_listening = False

    def process_command(self, cmd):
        if "time" in cmd:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}")
        elif "date" in cmd or "today" in cmd:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
        elif "who is" in cmd or "what is" in cmd:
            query = cmd.replace("who is", "").replace("what is", "").strip()
            try:
                info = wikipedia.summary(query, sentences=2)
                self.speak(info)
            except Exception:
                self.speak(f"Searching web for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "search" in cmd or "google" in cmd:
            query = cmd.replace("search", "").replace("google", "").strip()
            self.speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "youtube" in cmd:
            query = cmd.replace("youtube", "").replace("play", "").strip()
            self.speak(f"Opening YouTube for {query}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif "exit" in cmd or "stop" in cmd or "bye" in cmd:
            self.speak("Goodbye! Have a productive day.")
            self.root.after(1500, self.root.destroy)
        else:
            self.speak("I didn't recognize that command. Opening a web search.")
            webbrowser.open(f"https://www.google.com/search?q={cmd}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()