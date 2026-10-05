import sqlite3
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# --- Database Setup (SQLite) ---
def init_db():
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# --- Calculate BMI & Save to DB ---
def calculate_bmi():
    name = entry_name.get().strip()
    weight_str = entry_weight.get().strip()
    height_str = entry_height.get().strip()

    # Input Validation
    if not name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    try:
        weight = float(weight_str)
        height = float(height_str)

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be positive numbers.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")
        return

    # BMI Formula: weight (kg) / (height (m) ^ 2)
    bmi = weight / (height ** 2)
    bmi = round(bmi, 2)

    # Classify Category and Color
    if bmi < 18.5:
        category = "Underweight"
        color = "#1E90FF"  # Dodger Blue
    elif 18.5 <= bmi < 25:
        category = "Normal"
        color = "#2E8B57"  # Sea Green
    elif 25 <= bmi < 30:
        category = "Overweight"
        color = "#FFA500"  # Orange
    else:
        category = "Obese"
        color = "#DC143C"  # Crimson Red

    # Update GUI Display
    label_result.config(
        text=f"BMI: {bmi} ({category})",
        fg=color
    )

    # Save to SQLite Database
    try:
        conn = sqlite3.connect("bmi_records.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
            (name, weight, height, bmi, category)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save record: {e}")

# --- View Historical Trend Graph ---
def view_trend():
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("Error", "Enter a name to view historical BMI trend.")
        return

    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT bmi, date FROM records WHERE LOWER(name) = LOWER(?) ORDER BY id ASC", (name,))
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", f"No records found for '{name}'.")
        return

    bmi_values = [row[0] for row in data]
    attempts = list(range(1, len(bmi_values) + 1))

    # Matplotlib Graph Plotting
    plt.figure(figsize=(7, 4))
    plt.plot(attempts, bmi_values, marker='o', color='#4B0082', linewidth=2, label="BMI")
    plt.axhline(18.5, color='blue', linestyle='--', alpha=0.6, label='Underweight (<18.5)')
    plt.axhline(25, color='green', linestyle='--', alpha=0.6, label='Normal (18.5-24.9)')
    plt.axhline(30, color='red', linestyle='--', alpha=0.6, label='Obese (>=30)')
    plt.title(f"BMI History for {name}")
    plt.xlabel("Entry #")
    plt.ylabel("BMI")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

# --- Initialize DB ---
init_db()

# --- GUI Window ---
root = tk.Tk()
root.title("OIBSIP - BMI Calculator")
root.geometry("380x420")
root.resizable(False, False)

title_lbl = tk.Label(root, text="BMI Calculator", font=("Arial", 16, "bold"))
title_lbl.pack(pady=15)

# Form Fields
frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="User Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=6)
entry_name = tk.Entry(frame, width=22)
entry_name.grid(row=0, column=1, pady=6)

tk.Label(frame, text="Weight (kg):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=6)
entry_weight = tk.Entry(frame, width=22)
entry_weight.grid(row=1, column=1, pady=6)

tk.Label(frame, text="Height (m):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=6)
entry_height = tk.Entry(frame, width=22)
entry_height.grid(row=2, column=1, pady=6)

# Buttons
btn_calc = tk.Button(root, text="Calculate BMI", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=18, command=calculate_bmi)
btn_calc.pack(pady=12)

# Result Feedback
label_result = tk.Label(root, text="Enter details and click Calculate", font=("Arial", 11, "bold"), fg="gray")
label_result.pack(pady=8)

# Historical Trend Button
btn_trend = tk.Button(root, text="View BMI Trend", font=("Arial", 10), bg="#2196F3", fg="white", width=18, command=view_trend)
btn_trend.pack(pady=10)

root.mainloop()