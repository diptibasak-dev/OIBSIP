# AI Voice Assistant - Python Programming (Oasis Infobyte Internship)

An interactive desktop-based voice assistant built in Python that listens to spoken commands, processes natural language, and executes useful automated actions such as web searches, time/date inquiries, Wikipedia lookups, and media playback.

## 🚀 Features
- **Speech Recognition:** Captures live voice input from the microphone using Google's speech recognition API.
- **Text-to-Speech Feedback:** Responds back to the user via an offline voice synthesis engine (`pyttsx3`).
- **Dynamic Web Actions:** Opens popular platforms like Google, YouTube, GitHub, and Facebook directly via browser automation.
- **Information Retrieval:** Fetches real-time summaries of topics using the Wikipedia API.
- **Productivity & Utilities:** Tells the current time and date on request, along with built-in casual entertainment features (like jokes).
- **Interactive GUI:** Designed with an aesthetic dark-themed Tkinter dashboard featuring live status indicators (Idle, Listening, Processing).

---

## 🛠️ Tech Stack & Requirements
- **Language:** Python 3.x
- **GUI Framework:** Tkinter (Standard Library)
- **Audio & Speech:** `speech_recognition`, `pyttsx3`, `pyaudio`
- **Automation & APIs:** `webbrowser`, `wikipedia`, `requests`

### Installation
Install the required dependencies via terminal:
```bash
pip install -r requirements.txt