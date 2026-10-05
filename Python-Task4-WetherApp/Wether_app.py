import tkinter as tk
from tkinter import messagebox
import requests

def get_weather():
    city = entry_city.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    # Free API endpoint without requiring an API key
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            messagebox.showerror("Error", f"City '{city}' not found or service unavailable.")
            return

        data = response.json()
        current = data["current_condition"][0]

        temp_c = current["temp_C"]
        humidity = current["humidity"]
        desc = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]

        # Display results
        lbl_city_display.config(text=f"Weather in {city.capitalize()}", fg="#333333")
        lbl_temp.config(text=f"{temp_c} °C", fg="#FF5722")
        lbl_condition.config(text=f"Condition: {desc}", fg="#555555")
        lbl_details.config(text=f"Humidity: {humidity}% | Wind: {wind_speed} km/h", fg="#777777")

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Unable to connect to the internet. Please check your connection.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")

# --- GUI Window ---
root = tk.Tk()
root.title("OIBSIP - Basic Weather App")
root.geometry("400x380")
root.resizable(False, False)

# Title
title_lbl = tk.Label(root, text="Basic Weather App", font=("Arial", 16, "bold"))
title_lbl.pack(pady=15)

# Input Box
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="City Name:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
entry_city = tk.Entry(frame_input, font=("Arial", 11), width=18)
entry_city.grid(row=0, column=1, padx=5)

# Search Button
btn_search = tk.Button(root, text="Get Weather", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=15, command=get_weather)
btn_search.pack(pady=12)

# Weather Information Display
lbl_city_display = tk.Label(root, text="", font=("Arial", 13, "bold"))
lbl_city_display.pack(pady=5)

lbl_temp = tk.Label(root, text="", font=("Arial", 22, "bold"))
lbl_temp.pack(pady=3)

lbl_condition = tk.Label(root, text="", font=("Arial", 11))
lbl_condition.pack(pady=3)

lbl_details = tk.Label(root, text="", font=("Arial", 10))
lbl_details.pack(pady=5)

root.mainloop()