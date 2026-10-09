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

# Color Palette (Aesthetic Cyber Dark)
BG_MAIN = "#0B0F19"
CARD_BG = "#161F30"
BORDER_CLR = "#233048"
ACCENT_PRIMARY = "#6366F1"  # Indigo
ACCENT_ACTIVE = "#EF4444"   # Red during recording
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
USER_MSG_CLR = "#38BDF8"

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aura AI • Voice & Text Assistant")
        self.root.geometry("480x720")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_MAIN)

        # Initialize TTS Engine safely
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 165)
            voices = self.engine.getProperty("voices")
            if len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
        except Exception:
            self.engine = None

        self.is_listening = False
        self.setup_ui()
        self.speak_async("Hello! I am Aura, your assistant. You can speak or type your commands.")

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=(15, 8), padx=25)

        tk.Label(
            header,
            text="AURA ASSISTANT",
            font=("Helvetica", 13, "bold"),
            fg=TEXT_MAIN,
            bg=BG_MAIN
        ).pack(side="left")

        # Chat / Transcript Screen
        self.chat_card = tk.Frame(self.root, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER_CLR)
        self.chat_card.pack(fill="both", expand=True, padx=25, pady=8)

        self.chat_box = scrolledtext.ScrolledText(
            self.chat_card,
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            relief="flat",
            bd=0,
            padx=12,
            pady=12
        )
        self.chat_box.pack(fill="both", expand=True)
        self.chat_box.config(state="disabled")

        # Text Input Frame (Written Command Box)
        input_frame = tk.Frame(self.root, bg=BG_MAIN)
        input_frame.pack(fill="x", padx=25, pady=6)

        self.entry_text = Entry(
            input_frame,
            font=("Helvetica", 11),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER_CLR
        )
        self.entry_text.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self.entry_text.bind("<Return>", lambda e: self.handle_text_input())

        btn_send = tk.Button(
            input_frame,
            text="Send",
            command=self.handle_text_input,
            font=("Helvetica", 9, "bold"),
            bg=ACCENT_PRIMARY,
            fg=TEXT_MAIN,
            activebackground="#4F46E5",
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_send.pack(side="right")

        # Bottom Controls (Microphone & Status)
        controls = tk.Frame(self.root, bg=BG_MAIN)
        controls.pack(fill="x", padx=25, pady=(6, 20))

        self.lbl_status = tk.Label(
            controls,
            text="Status: Idle",
            font=("Helvetica", 9),
            bg=BG_MAIN,
            fg=TEXT_MUTED
        )
        self.lbl_status.pack(pady=2)

        self.btn_mic = tk.Button(
            controls,
            text="🎙️ Tap to Speak",
            command=self.trigger_listening,
            font=("Helvetica", 10, "bold"),
            bg=ACCENT_PRIMARY,
            fg=TEXT_MAIN,
            activebackground="#4F46E5",
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8
        )
        self.btn_mic.pack(pady=4)

    def log_message(self, sender, text):
        def _update():
            self.chat_box.config(state="normal")
            self.chat_box.insert(tk.END, f"{sender}: {text}\n\n")
            self.chat_box.see(tk.END)
            self.chat_box.config(state="disabled")
        self.root.after(0, _update)

    def speak(self, text):
        self.log_message("Aura", text)
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

    def speak_async(self, text):
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    def handle_text_input(self):
        text = self.entry_text.get().strip()
        if not text:
            return
        self.entry_text.delete(0, tk.END)
        self.log_message("You (Typed)", text)
        threading.Thread(target=self.execute_command, args=(text.lower(),), daemon=True).start()

    def trigger_listening(self):
        if not self.is_listening:
            threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        self.is_listening = True
        self.root.after(0, lambda: self.lbl_status.config(text="Status: Listening...", fg=USER_MSG_CLR))
        self.root.after(0, lambda: self.btn_mic.config(bg=ACCENT_ACTIVE, text="Listening..."))

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                self.root.after(0, lambda: self.lbl_status.config(text="Status: Processing...", fg=ACCENT_PRIMARY))
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                cmd = recognizer.recognize_google(audio).lower()
                self.log_message("You (Voice)", cmd)
                self.execute_command(cmd)
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything.")
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand that.")
        except Exception:
            self.speak("Microphone or network connection error.")

        self.root.after(0, lambda: self.lbl_status.config(text="Status: Idle", fg=TEXT_MUTED))
        self.root.after(0, lambda: self.btn_mic.config(bg=ACCENT_PRIMARY, text="🎙️ Tap to Speak"))
        self.is_listening = False

    def execute_command(self, cmd):
        if hasattr(self, '_last_cmd') and self._last_cmd == cmd:
            return
        self._last_cmd = cmd

        # 1. Greetings & Casual Chat (No browser open)
        if cmd in ["hi", "hello", "hey", "hii", "gm", "good morning"]:
            self.speak("Hello! How can I help you today?")
        elif "kemon acho" in cmd or "how are you" in cmd:
            self.speak("Ami valo achhi! Apni kemon achen?")
        elif "thank you" in cmd or "thanks" in cmd:
            self.speak("You're welcome! Let me know if you need anything else.")
        
        # 2. Time & Date
        elif "time" in cmd:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}")
        elif "date" in cmd or "today" in cmd:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
        
        # 3. Open System Apps & Tools
        elif "notepad" in cmd:
            self.speak("Opening Notepad")
            subprocess.Popen(["notepad.exe"])
        elif "calculator" in cmd or "calc" in cmd:
            self.speak("Opening Calculator")
            subprocess.Popen(["calc.exe"])
        elif "paint" in cmd:
            self.speak("Opening Paint")
            subprocess.Popen(["mspaint.exe"])
        elif "command prompt" in cmd or "cmd" in cmd:
            self.speak("Opening Command Prompt")
            subprocess.Popen(["cmd.exe"])
        elif "explorer" in cmd or "files" in cmd or "this pc" in cmd:
            self.speak("Opening File Explorer")
            subprocess.Popen(["explorer.exe"])
        elif "task manager" in cmd:
            self.speak("Opening Task Manager")
            subprocess.Popen(["taskmgr.exe"])
        elif "control panel" in cmd:
            self.speak("Opening Control Panel")
            subprocess.Popen(["control.exe"])
        elif "media player" in cmd or "windows media player" in cmd:
            self.speak("Opening Media Player")
            subprocess.Popen(["wmplayer.exe"])
        elif "settings" in cmd:
            self.speak("Opening Windows Settings")
            subprocess.Popen(["start", "ms-settings:"], shell=True)
        elif "visual studio code" in cmd or "vs code" in cmd or "code" in cmd:
            self.speak("Opening Visual Studio Code")
            subprocess.Popen(["code"])
        elif "word" in cmd or "microsoft word" in cmd:
            self.speak("Opening Microsoft Word")
            subprocess.Popen(["winword.exe"])
        elif "excel" in cmd or "microsoft excel" in cmd:
            self.speak("Opening Microsoft Excel")
            subprocess.Popen(["excel.exe"])
        elif "powershell" in cmd:
            self.speak("Opening PowerShell")
            subprocess.Popen(["powershell.exe"])
        elif "camera" in cmd:
            self.speak("Opening Camera")
            subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
        elif "snipping tool" in cmd or "screenshot tool" in cmd:
            self.speak("Opening Snipping Tool")
            subprocess.Popen(["SnippingTool.exe"])
        
        # 4. Open Specific Websites & Social Media
        elif cmd in ["open github", "github"]:
            self.speak("Opening GitHub")
            webbrowser.open("https://github.com", new=2)
        elif cmd in ["open youtube", "youtube"]:
            self.speak("Opening YouTube")
            webbrowser.open("https://youtube.com", new=2)
        elif cmd in ["open facebook", "facebook"]:
            self.speak("Opening Facebook")
            webbrowser.open("https://facebook.com", new=2)
        elif cmd in ["open chatgpt", "chatgpt"]:
            self.speak("Opening ChatGPT")
            webbrowser.open("https://chatgpt.com", new=2)
        elif cmd in ["open instagram", "instagram"]:
            self.speak("Opening Instagram")
            webbrowser.open("https://instagram.com", new=2)
        elif cmd in ["open spotify", "spotify"]:
            self.speak("Opening Spotify")
            webbrowser.open("https://open.spotify.com", new=2)
        elif cmd in ["open twitter", "open x", "twitter", "x"]:
            self.speak("Opening Twitter")
            webbrowser.open("https://twitter.com", new=2)
        elif cmd in ["open linkedin", "linkedin"]:
            self.speak("Opening LinkedIn")
            webbrowser.open("https://linkedin.com", new=2)
        elif cmd in ["open reddit", "reddit"]:
            self.speak("Opening Reddit")
            webbrowser.open("https://reddit.com", new=2)
        elif cmd in ["open whatsapp", "whatsapp"]:
            self.speak("Opening WhatsApp Web")
            webbrowser.open("https://web.whatsapp.com", new=2)
        
        # 5. YouTube Video Play / Search
        elif "play" in cmd or ("youtube" in cmd and len(cmd) > 7):
            query = cmd.replace("youtube", "").replace("play", "").strip()
            self.speak(f"Playing {query if query else 'videos'} on YouTube")
            url = f"https://www.youtube.com/results?search_query={query}" if query else "https://www.youtube.com"
            webbrowser.open(url, new=2)
        
        # 6. Wikipedia Information
        elif "who is" in cmd or "what is" in cmd or "tell me about" in cmd:
            query = cmd.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                self.speak(summary)
            except Exception:
                self.speak(f"Searching web for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}", new=2)
        
        # 7. General Google Search
        elif "search" in cmd or "google" in cmd:
            query = cmd.replace("search", "").replace("google", "").strip()
            self.speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}", new=2)
        
        # 8. Fun Feature: Jokes
        elif "joke" in cmd:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the computer sneeze? Because it had a virus!",
                "In a world of algorithms, be a human!"
            ]
            self.speak(random.choice(jokes))
            
        # 9. Exit Command
        elif "exit" in cmd or "stop" in cmd or "bye" in cmd:
            self.speak("Goodbye! Have a great day.")
            self.root.after(1500, self.root.destroy)
            
        # 10. Fallback (Safe response without random browser opening)
        else:
            self.speak(f"I am not sure about '{cmd}'. You can ask me to search Google or open an app.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()