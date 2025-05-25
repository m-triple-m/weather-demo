# import network
# import time
# import requests
# from machine import Pin, I2C
# import dht
# import ssd1306  # Ensure ssd1306.py is uploaded to the device

# # === Wi-Fi Credentials ===
# SSID = "Digipodium_4G"
# PASSWORD = "digipod@123"

# # === Firebase Realtime DB URL ===
# FIREBASE_URL = "https://iot-demo-c17cb-default-rtdb.firebaseio.com/weather.json"

# # === Setup OLED Display ===
# # I2C pins for ESP8266: D1 (SCL = GPIO5), D2 (SDA = GPIO4)
# i2c = I2C(scl=Pin(5), sda=Pin(4))  # Adjust pins if using different board
# oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# # === DHT11 Sensor on D4 (GPIO2) ===
# sensor = dht.DHT11(Pin(2))

# # === Connect to Wi-Fi ===
# def connect_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     if not wlan.isconnected():
#         print("Connecting to WiFi...", end="")
#         wlan.connect(SSID, PASSWORD)
#         while not wlan.isconnected():
#             print(".", end="")
#             time.sleep(1)
#     print("\nConnected to:", SSID)
#     print("IP address:", wlan.ifconfig()[0])
#     oled.fill(0)
#     oled.text("WiFi Connected", 0, 0)
#     oled.text(wlan.ifconfig()[0], 0, 10)
#     oled.show()

# # === Send Data to Firebase ===
# def send_to_firebase(temp, hum):
#     data = {
#         "temperature": temp,
#         "humidity": hum,
#         "timestamp": time.time()
#     }
#     try:
#         res = requests.put(FIREBASE_URL, json=data)
#         print("Sent to Firebase:", res.text)
#         res.close()
#     except Exception as e:
#         print("Error sending to Firebase:", e)

# # === Update OLED Display ===
# def update_display(temp, hum):
#     oled.fill(0)
#     oled.text("Weather Station", 0, 0)
#     oled.text("--------------", 0, 10)
#     oled.text("Temperature:", 0, 20)
#     oled.text("{} C".format(temp), 90, 20)
#     oled.text("Humidity:", 0, 35)
#     oled.text("{} %".format(hum), 90, 35)
#     oled.text("Updated: {}".format(time.localtime()[4:6]), 0, 50)
#     oled.show()

# # === Main Execution ===
# connect_wifi()

# while True:
#     try:
#         sensor.measure()
#         temp = sensor.temperature()
#         hum = sensor.humidity()
#         print("Temperature:", temp, "C | Humidity:", hum, "%")

#         update_display(temp, hum)
#         send_to_firebase(temp, hum)

#     except Exception as e:
#         print("Sensor error:", e)

#     time.sleep(10)
