import tkinter as tk
from tkinter import messagebox, Toplevel
import requests

# No API Key, No Registration Required! Uses public wttr.in service.

BG_MAIN = "#F8FAFC"
CARD_BG = "#FFFFFF"
BORDER_COLOR = "#E2E8F0"
ACCENT_BLUE = "#0EA5E9"
ACCENT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"

class NoKeyWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("440x680")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_MAIN)

        self.unit = "metric"  # 'metric' = °C, 'imperial' = °F
        self.current_city = ""
        self.raw_data = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            header,
            text="LIVE WEATHER",
            font=("Helvetica", 11, "bold"),
            fg=ACCENT_DARK,
            bg=BG_MAIN
        ).pack(side="left")

        self.btn_unit = tk.Button(
            header,
            text="°C / °F",
            command=self.toggle_unit,
            font=("Helvetica", 9, "bold"),
            bg=CARD_BG,
            fg=ACCENT_BLUE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4
        )
        self.btn_unit.pack(side="right")

        # Search Box
        search_frame = tk.Frame(self.root, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER_COLOR)
        search_frame.pack(fill="x", padx=25, pady=10, ipady=4)

        self.entry_city = tk.Entry(
            search_frame,
            font=("Helvetica", 11),
            bg=CARD_BG,
            fg=ACCENT_DARK,
            relief="flat",
            bd=0
        )
        self.entry_city.pack(side="left", padx=12, fill="x", expand=True)
        self.entry_city.bind("<Return>", lambda e: self.fetch_weather())

        btn_search = tk.Button(
            search_frame,
            text="Search",
            command=self.fetch_weather,
            font=("Helvetica", 9, "bold"),
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=6
        )
        btn_search.pack(side="right", padx=4)

        # Action row
        action_row = tk.Frame(self.root, bg=BG_MAIN)
        action_row.pack(fill="x", padx=25, pady=6)

        btn_loc = tk.Button(
            action_row,
            text="📍 Auto GPS",
            command=self.auto_locate,
            font=("Helvetica", 8, "bold"),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        btn_loc.pack(side="left")

        btn_5d = tk.Button(
            action_row,
            text="📅 3-Day Forecast",
            command=self.open_forecast_window,
            font=("Helvetica", 8, "bold"),
            bg=CARD_BG,
            fg=ACCENT_BLUE,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        btn_5d.pack(side="right")

        # Hero Card
        self.hero_card = tk.Frame(self.root, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.hero_card.pack(fill="x", padx=25, pady=15, ipady=12)

        self.lbl_city = tk.Label(
            self.hero_card,
            text="Enter Any City",
            font=("Helvetica", 16, "bold"),
            bg=CARD_BG,
            fg=ACCENT_DARK
        )
        self.lbl_city.pack(pady=(12, 2))

        self.lbl_desc = tk.Label(
            self.hero_card,
            text="No API Key or login required!",
            font=("Helvetica", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED
        )
        self.lbl_desc.pack(pady=(0, 10))

        self.lbl_temp = tk.Label(
            self.hero_card,
            text="--°",
            font=("Helvetica", 40, "bold"),
            bg=CARD_BG,
            fg=ACCENT_BLUE
        )
        self.lbl_temp.pack(pady=6)

        metrics_strip = tk.Frame(self.hero_card, bg="#F1F5F9")
        metrics_strip.pack(fill="x", padx=16, pady=(15, 5), ipady=8)

        self.lbl_humidity = tk.Label(
            metrics_strip,
            text="💧 Humidity: --",
            font=("Helvetica", 9),
            bg="#F1F5F9",
            fg=TEXT_MUTED
        )
        self.lbl_humidity.pack(side="left", expand=True)

        self.lbl_wind = tk.Label(
            metrics_strip,
            text="💨 Wind: --",
            font=("Helvetica", 9),
            bg="#F1F5F9",
            fg=TEXT_MUTED
        )
        self.lbl_wind.pack(side="left", expand=True)

        tk.Label(
            self.root,
            text="Powered by Public Weather Engine",
            font=("Helvetica", 8),
            bg=BG_MAIN,
            fg=TEXT_MUTED
        ).pack(side="bottom", pady=15)

    def toggle_unit(self):
        if self.unit == "metric":
            self.unit = "imperial"
            self.btn_unit.config(text="Unit: °F")
        else:
            self.unit = "metric"
            self.btn_unit.config(text="Unit: °C")

        if self.current_city:
            self.fetch_weather()

    def auto_locate(self):
        try:
            res = requests.get("https://ipinfo.io/json", timeout=4).json()
            city = res.get("city")
            if city:
                self.entry_city.delete(0, tk.END)
                self.entry_city.insert(0, city)
                self.fetch_weather()
            else:
                messagebox.showerror("Error", "Auto location failed.")
        except Exception:
            messagebox.showerror("Network Error", "Unable to detect location.")

    def fetch_weather(self):
        city = self.entry_city.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        url = f"https://wttr.in/{city}?format=j1"
        try:
            resp = requests.get(url, timeout=6)
            if resp.status_code != 200:
                messagebox.showerror("Error", "City not found or network error.")
                return

            data = resp.json()
            self.current_city = city
            self.raw_data = data

            current = data["current_condition"][0]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]

            if self.unit == "metric":
                temp = f"{current['temp_C']}°C"
                wind = f"{current['windspeedKmph']} km/h"
            else:
                temp = f"{current['temp_F']}°F"
                wind = f"{current['windspeedMiles']} mph"

            self.lbl_city.config(text=city.title())
            self.lbl_desc.config(text=desc)
            self.lbl_temp.config(text=temp)
            self.lbl_humidity.config(text=f"💧 Humidity: {humidity}%")
            self.lbl_wind.config(text=f"💨 Wind: {wind}")

        except Exception:
            messagebox.showerror("Error", "Could not fetch weather data.")

    def open_forecast_window(self):
        if not self.raw_data:
            messagebox.showwarning("Warning", "Please search for a city first!")
            return

        win = Toplevel(self.root)
        win.title(f"Forecast • {self.current_city}")
        win.geometry("360x420")
        win.configure(bg=BG_MAIN)

        tk.Label(win, text=f"3-Day Weather Forecast", font=("Helvetica", 11, "bold"), bg=BG_MAIN, fg=ACCENT_DARK).pack(pady=12)

        try:
            weather_days = self.raw_data.get("weather", [])
            for day in weather_days:
                date_str = day["date"]
                max_c = day["maxtempC"]
                min_c = day["mintempC"]
                max_f = day["maxtempF"]
                min_f = day["mintempF"]
                
                if self.unit == "metric":
                    temp_str = f"Max: {max_c}°C / Min: {min_c}°C"
                else:
                    temp_str = f"Max: {max_f}°F / Min: {min_f}°F"

                card = tk.Frame(win, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER_COLOR)
                card.pack(fill="x", padx=20, pady=6, ipady=6)

                tk.Label(card, text=date_str, font=("Helvetica", 9, "bold"), bg=CARD_BG, fg=ACCENT_DARK).pack(side="left", padx=15)
                tk.Label(card, text=temp_str, font=("Helvetica", 9, "bold"), bg=CARD_BG, fg=ACCENT_BLUE).pack(side="right", padx=15)
        except Exception:
            tk.Label(win, text="Forecast data unavailable.", bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = NoKeyWeatherApp(root)
    root.mainloop()