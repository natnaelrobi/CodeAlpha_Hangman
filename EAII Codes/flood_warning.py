from datetime import datetime
import winsound
import requests

CITIES = {
    "Addis Ababa": (9.02497, 38.74689),
    "Bahir Dar": (11.5936, 37.3908),
    "Dire Dawa": (9.5931, 41.8661),
    "Hawassa": (7.0621, 38.4763),
    "Jimma": (7.6731, 36.8344),
    "Mekelle": (13.4967, 39.4753),
    "Gondar": (12.6000, 37.4667),
    "Adama": (8.5400, 39.2700),
    "Arba Minch": (6.0333, 37.5500),
    "Dessie": (11.1333, 39.6333),
    "Jijiga": (9.3500, 42.8000),
    "Gambela": (8.2500, 34.5833),
    "Asosa": (10.0667, 34.5333),
    "Semera": (11.7944, 41.0056),
    "Harar": (9.3139, 42.1181),
    "Bishoftu": (8.7500, 38.9833),
    "Dilla": (6.4167, 38.3167),
    "Nekemte": (9.0833, 36.5500),
}

class FloodDetector:

  def __init__(self, threshold=10):
    self.threshold = threshold

  def play_alert_beeps(self):
    print("🚨 SOUNDING EMERGENCY ALERT BEEPS...")
    for i in range(3):
      winsound.Beep(1800, 400)

  def fetch_rainfall_data(self, city_name):
    lat, lon = CITIES[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation&hourly=precipitation"

    try:
      response = requests.get(url, timeout=5)
      data = response.json()
      current_rain = data["current"]["precipitation"]
      hourly_rain = data["hourly"]["precipitation"][:24]
      max_24h_rain = max(hourly_rain)
      return current_rain, max_24h_rain
    except Exception as error:
      print(f"❌ Network Error for {city_name}: {error}")
      return None, None

  def check_city(self, city_name):
    current_rain, max_24h_rain = self.fetch_rainfall_data(city_name)

    if current_rain is None:
      return

    print(f"\n==============================")
    print(f"📍 Checking City: {city_name}")
    print(f"🌧️ Current Rainfall: {current_rain} mm/hr")
    print(f"🔮 Max Rain (Next 24h): {max_24h_rain} mm/hr")

    if current_rain >= self.threshold or max_24h_rain >= self.threshold:
      status = "🚨 DANGER: Flood Warning Alert!"
      print(f"Status: {status}")
      self.play_alert_beeps()
    else:
      status = "✅ SAFE: Conditions Normal"
      print(f"Status: {status}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] City: {city_name} | Current: {current_rain} mm | 24h Max: {max_24h_rain} mm | Status: {status}\n"

    with open("flood_log.txt", "a", encoding="utf-8") as file:
      file.write(log_line)

    print("📄 Saved entry to flood_log.txt")
    print(f"==============================\n")


if __name__ == "__main__":
  detector = FloodDetector(threshold=10)
  detector.check_city("Addis Ababa")