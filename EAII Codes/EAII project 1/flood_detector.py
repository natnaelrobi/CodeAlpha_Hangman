import csv
import os
import winsound
import requests

class FloodDetector:

  def __init__(self, hourly_threshold=15.0, daily_threshold=50.0):
    self.hourly_threshold = hourly_threshold
    self.daily_threshold = daily_threshold
    self.cities = self.load_cities()

  def load_cities(self):
    cities = {}
    file = open("cities.csv", "r")
    reader = csv.DictReader(file)

    for row in reader:
      city = row["City"].strip().title()
      lat = float(row["Latitude"])
      lon = float(row["Longitude"])
      cities[city] = (lat, lon)

    file.close()
    return cities

  def play_alert_beeps(self):
    print("SOUNDING EMERGENCY ALERT BEEPS...")
    for i in range(3):
      winsound.Beep(1800, 400)

  def check_city(self, user_input):
    city_name = user_input.strip().title()

    if city_name not in self.cities:
      print("Error: City not found in cities.csv records.")
      return

    lat, lon = self.cities[city_name]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation&hourly=precipitation"
    response = requests.get(url)
    data = response.json()

    current_rain = data["current"]["precipitation"]
    hourly_rain = data["hourly"]["precipitation"][:24]

    max_hourly_rain = max(hourly_rain)
    total_24h_rain = sum(hourly_rain)

    print("\n"+"="*30)
    print("Checking City:", city_name)
    print("Current Rainfall:", current_rain, "mm")
    print("Peak Hourly Rain:", max_hourly_rain, "mm/hr")
    print("24 hour Cumulative Rain:", round(total_24h_rain, 1), "mm")

    if (max_hourly_rain >= self.hourly_threshold
        or total_24h_rain >= self.daily_threshold):
      status = "DANGER: Flood Warning Alert!"
      print("Status:", status)
      self.play_alert_beeps()
    else:
      status = "SAFE: Conditions Normal"
      print("Status:", status)

    self.log_to_csv(city_name, current_rain, max_hourly_rain, total_24h_rain, status)
    print("Saved entry to flood_log.csv")
    print("\n"+"="*30)

  def log_to_csv(self, city_name, current_rain, max_hourly_rain, total_24h_rain, status):
    file_exists = os.path.exists("flood_log.csv")

    file = open("flood_log.csv", "a", newline="")
    writer = csv.writer(file)

    if not file_exists:
      writer.writerow([
          "City",
          "Current_Rain_mm",
          "Peak_Hourly_mm",
          "Total_24h_mm",
          "Status",
      ])

    writer.writerow([city_name, current_rain, max_hourly_rain, total_24h_rain, status])
    file.close()

if __name__ == "__main__":
  detector = FloodDetector()
  user_city = input("Enter city name: ")
  detector.check_city(user_city)