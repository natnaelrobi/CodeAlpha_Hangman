import csv
from datetime import datetime
import os
import winsound
import requests


class FloodDetector:

  def __init__(
      self,
      cities_file="cities.csv",
      hourly_threshold=15.0,
      daily_threshold=50.0,
  ):
    self.hourly_threshold = hourly_threshold
    self.daily_threshold = daily_threshold
    self.cities_file = cities_file
    self.cities = self.load_cities()

  def load_cities(self):
    cities = {}
    if not os.path.exists(self.cities_file):
      print(f"❌ Error: Local file '{self.cities_file}' was not found.")
      return cities

    try:
      with open(self.cities_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
          city = row["City"].strip().title()
          lat = float(row["Latitude"])
          lon = float(row["Longitude"])
          cities[city] = (lat, lon)
    except UnicodeDecodeError:
      with open(self.cities_file, "r", encoding="cp1252") as file:
        reader = csv.DictReader(file)
        for row in reader:
          city = row["City"].strip().title()
          lat = float(row["Latitude"])
          lon = float(row["Longitude"])
          cities[city] = (lat, lon)

    return cities

  def play_alert_beeps(self):
    print("🚨 SOUNDING EMERGENCY ALERT BEEPS...")
    for i in range(3):
      winsound.Beep(1800, 400)

  def fetch_rainfall_data(self, lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation&hourly=precipitation"

    try:
      response = requests.get(url, timeout=5)
      data = response.json()
      current_rain = data["current"]["precipitation"]
      hourly_rain = data["hourly"]["precipitation"][:24]
      max_hourly_rain = max(hourly_rain)
      total_24h_rain = sum(hourly_rain)
      return current_rain, max_hourly_rain, total_24h_rain
    except Exception as error:
      print(f"❌ Network Error: {error}")
      return None, None, None

  def check_city(self, user_input):
    city_name = user_input.strip().title()

    if city_name not in self.cities:
      print(
          f"❌ City '{city_name}' was not found in '{self.cities_file}'"
          " records."
      )
      return

    lat, lon = self.cities[city_name]
    current_rain, max_hourly_rain, total_24h_rain = self.fetch_rainfall_data(
        lat, lon
    )

    if current_rain is None:
      return

    print(f"\n==============================")
    print(f"📍 Checking City: {city_name}")
    print(f"🌧️ Current Rainfall: {current_rain} mm")
    print(f"⚡ Peak Hourly Rain (Next 24h): {max_hourly_rain} mm/hr")
    print(f"🌊 Cumulative Rain (Next 24h): {total_24h_rain:.1f} mm")

    if (
        max_hourly_rain >= self.hourly_threshold
        or total_24h_rain >= self.daily_threshold
    ):
      status = "🚨 DANGER: Flood Warning Alert!"
      print(f"Status: {status}")
      self.play_alert_beeps()
    else:
      status = "✅ SAFE: Conditions Normal"
      print(f"Status: {status}")

    self.log_to_csv(
        city_name, current_rain, max_hourly_rain, total_24h_rain, status
    )
    print("📄 Saved entry to flood_log.csv")
    print(f"==============================\n")

  def log_to_csv(
      self, city_name, current_rain, max_hourly_rain, total_24h_rain, status
  ):
    file_exists = os.path.exists("flood_log.csv")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("flood_log.csv", "a", newline="", encoding="utf-8") as file:
      writer = csv.writer(file)
      if not file_exists:
        writer.writerow([
            "Timestamp",
            "City",
            "Current_Rain_mm",
            "Peak_Hourly_mm",
            "Total_24h_mm",
            "Status",
        ])
      writer.writerow([
          now,
          city_name,
          current_rain,
          max_hourly_rain,
          round(total_24h_rain, 1),
          status,
      ])


if __name__ == "__main__":
  hourly_input = input(
      "Enter peak hourly threshold in mm/hr (if you don't know, press Enter"
      " for default 15): "
  ).strip()
  daily_input = input(
      "Enter 24h cumulative threshold in mm (if you don't know, press Enter"
      " for default 50): "
  ).strip()

  try:
    hourly_val = float(hourly_input) if hourly_input else 15.0
  except ValueError:
    hourly_val = 15.0

  try:
    daily_val = float(daily_input) if daily_input else 50.0
  except ValueError:
    daily_val = 50.0

  detector = FloodDetector(
      hourly_threshold=hourly_val, daily_threshold=daily_val
  )
  user_city = input("Enter city name: ")
  detector.check_city(user_city)
