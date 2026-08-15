from datetime import datetime
import threading
import time
import tkinter as tk
from tkinter import messagebox
import winsound
import requests

# ─── MULTI-CITY DATABASE ───────────────────────────────────────────────────
CITIES = {
    "Addis Ababa": (9.02497, 38.74689),
    "Bahir Dar": (11.5936, 37.3908),
    "Dire Dawa": (9.5931, 41.8661),
    "Hawassa": (7.0621, 38.4763),
    "Jimma": (7.6731, 36.8344),
}

THRESHOLD = 10.0  # mm/hr threshold for flood danger


# ─── OBJECT-ORIENTED PROGRAMMING (CLASS) ──────────────────────────────────
class FloodMonitorApp:

  def __init__(self):
    # Setup Tkinter Window
    self.root = tk.Tk()
    self.root.title("🌧️ Flood Early Warning System")
    self.root.geometry("450x600")
    self.root.configure(bg="#f4f6f9")

    # Alarm state variables
    self.alarm_active = False

    # Selected City Variable
    self.selected_city = tk.StringVar(value="Addis Ababa")

    # Handle window close to ensure sound stops
    self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # Build the User Interface
    self.create_widgets()

  def create_widgets(self):
    """Builds the Tkinter visual layout."""
    # Header Banner
    title_label = tk.Label(
        self.root,
        text="FLOOD EARLY WARNING SYSTEM",
        font=("Arial", 15, "bold"),
        bg="#2c3e50",
        fg="white",
        pady=12,
    )
    title_label.pack(fill="x")

    # City Selector Dropdown
    city_frame = tk.Frame(self.root, bg="#f4f6f9", pady=10)
    city_frame.pack()

    tk.Label(
        city_frame,
        text="Select City:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f9",
    ).pack(side="left", padx=5)
    city_dropdown = tk.OptionMenu(
        city_frame, self.selected_city, *CITIES.keys()
    )
    city_dropdown.config(font=("Arial", 10), bg="white")
    city_dropdown.pack(side="left", padx=5)

    # Visual Status Card
    self.status_card = tk.Label(
        self.root,
        text="READY TO CHECK",
        font=("Arial", 13, "bold"),
        bg="#3498db",
        fg="white",
        width=32,
        height=3,
        relief="groove",
    )
    self.status_card.pack(pady=10)

    # 🚨 MUTE BUTTON (Hidden by default)
    self.mute_btn = tk.Button(
        self.root,
        text="🔇 SILENCE EMERGENCY ALARM",
        font=("Arial", 11, "bold"),
        bg="#c0392b",
        fg="white",
        width=28,
        height=2,
        command=self.stop_alarm,
    )

    # Weather Metrics Panel
    metrics_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
    metrics_frame.pack(padx=20, pady=5, fill="x")

    self.current_rain_label = tk.Label(
        metrics_frame,
        text="Current Rainfall: -- mm/hr",
        font=("Arial", 11),
        bg="white",
        anchor="w",
    )
    self.current_rain_label.pack(fill="x", padx=15, pady=6)

    # 24-Hour Forecast Label
    self.forecast_label = tk.Label(
        metrics_frame,
        text="Max Rain Next 24h: -- mm/hr",
        font=("Arial", 11),
        bg="white",
        anchor="w",
    )
    self.forecast_label.pack(fill="x", padx=15, pady=6)

    # Buttons Section
    btn_frame = tk.Frame(self.root, bg="#f4f6f9")
    btn_frame.pack(pady=15)

    check_btn = tk.Button(
        btn_frame,
        text="🌧️ Check Live Weather",
        font=("Arial", 11, "bold"),
        bg="#27ae60",
        fg="white",
        width=25,
        command=self.check_weather,
    )
    check_btn.pack(pady=4)

    # Simulation / Demo Mode Button
    test_btn = tk.Button(
        btn_frame,
        text="⚠️ Test Mode (Simulate Flood)",
        font=("Arial", 10),
        bg="#e67e22",
        fg="white",
        width=25,
        command=self.simulate_alert,
    )
    test_btn.pack(pady=4)

    # Historical Log Statistics Button
    stats_btn = tk.Button(
        btn_frame,
        text="📊 View History Log Stats",
        font=("Arial", 10),
        bg="#8e44ad",
        fg="white",
        width=25,
        command=self.show_log_stats,
    )
    stats_btn.pack(pady=4)

  # ─── AUDIO ALARM METHODS ──────────────────────────────────────────────────
  def start_alarm(self):
    """Starts continuous background alarm beeping."""
    if not self.alarm_active:
      self.alarm_active = True
      self.mute_btn.pack(pady=5)
      threading.Thread(target=self._siren_loop, daemon=True).start()

  def _siren_loop(self):
    """Looping audio tones that sound like an emergency siren."""
    while self.alarm_active:
      winsound.Beep(2000, 250)  # High pitch beep
      time.sleep(0.05)
      winsound.Beep(1400, 250)  # Lower pitch beep
      time.sleep(0.05)

  def stop_alarm(self):
    """Stops the audio alarm and hides the silence button."""
    self.alarm_active = False
    self.mute_btn.pack_forget()

  # ─── WEATHER LOGIC ───────────────────────────────────────────────────────
  def fetch_data(self, lat, lon):
    """Gets current and hourly weather data from Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation&hourly=precipitation&timezone=auto"
    response = requests.get(url, timeout=5)
    return response.json()

  def process_weather(self, current_rain, max_forecast):
    """Processes threshold logic, updates Tkinter UI, and logs to file."""
    city = self.selected_city.get()

    if current_rain >= THRESHOLD:
      status = "🚨 DANGER: FLOOD ALERT!"
      card_color = "#e74c3c"  # Red
      self.start_alarm()
    elif max_forecast >= THRESHOLD:
      status = "⚠️ WARNING: Heavy Rain Expected Soon!"
      card_color = "#f39c12"  # Orange
      self.stop_alarm()
    else:
      status = "✅ SAFE: Normal Conditions"
      card_color = "#2ecc71"  # Green
      self.stop_alarm()

    # Update UI Components
    self.status_card.config(text=status, bg=card_color)
    self.current_rain_label.config(
        text=f"Current Rainfall: {current_rain} mm/hr"
    )
    self.forecast_label.config(text=f"Max Rain Next 24h: {max_forecast} mm/hr")

    # Log Check to File (encoding='utf-8' prevents Windows Unicode errors)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] City: {city} | Current: {current_rain} mm | 24h Max: {max_forecast} mm | Status: {status}\n"

    with open("flood_log.txt", "a", encoding="utf-8") as file:
      file.write(log_line)

  def check_weather(self):
    """Handles the Live Weather button click."""
    city = self.selected_city.get()
    lat, lon = CITIES[city]

    try:
      data = self.fetch_data(lat, lon)
      current_rain = data["current"]["precipitation"]
      hourly_rain = data["hourly"]["precipitation"][:24]
      max_forecast = max(hourly_rain)
    except Exception:
      messagebox.showerror(
          "Connection Error",
          "Could not fetch weather data. Please check your internet connection.",
      )
      return

    self.process_weather(current_rain, max_forecast)

  def simulate_alert(self):
    """Simulates high rainfall for live presentation testing."""
    self.process_weather(current_rain=14.5, max_forecast=18.0)

  def show_log_stats(self):
    """Reads flood_log.txt and displays summary statistics."""
    try:
      with open("flood_log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

      total_checks = len(lines)
      danger_alerts = sum(1 for line in lines if "DANGER" in line)
      warnings = sum(1 for line in lines if "WARNING" in line)
      safe_checks = total_checks - danger_alerts - warnings

      stats_msg = (
          f"📋 Total Checks Performed: {total_checks}\n\n"
          f"🚨 Flood Danger Alerts: {danger_alerts}\n"
          f"⚠️ Heavy Rain Warnings: {warnings}\n"
          f"✅ Safe Conditions: {safe_checks}"
      )
      messagebox.showinfo("Historical Log Statistics", stats_msg)
    except FileNotFoundError:
      messagebox.showwarning(
          "No Log File", "No log records found yet. Run a check first!"
      )

  def on_close(self):
    """Ensure sound thread stops when closing window."""
    self.stop_alarm()
    self.root.destroy()

  def run(self):
    self.root.mainloop()


if __name__ == "__main__":
  app = FloodMonitorApp()
  app.run()