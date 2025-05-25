import machine
import time
import dht
import ssd1306

# === Pins Setup ===
dht_sensor = dht.DHT11(machine.Pin(2))  # D4
mq135_pin = machine.ADC(0)              # A0
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))  # D1, D2
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Simulated Mapping Function ===
def estimate_gases(raw):
    # These ranges are simulated; real values require calibration
    co2 = int(raw * 0.4)      # Simulate CO2 PPM
    co = int(raw * 0.3)       # Simulate CO PPM
    nh3 = int(raw * 0.2)      # Simulate NH3 PPM
    return co2, co, nh3

def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        gas_raw = mq135_pin.read()
        co2, co, nh3 = estimate_gases(gas_raw)
        return temp, hum, co2, co, nh3
    except Exception as e:
        print("Error:", e)
        return None, None, None, None, None

def display(temp, hum, co2, co, nh3):
    oled.fill(0)
    oled.text("T:{}C H:{}%".format(temp, hum), 0, 0)
    oled.text("CO2 : {}".format(co2), 0, 15)
    oled.text("CO  : {}".format(co), 0, 30)
    oled.text("NH3 : {}".format(nh3), 0, 45)
    oled.show()

while True:
    temp, hum, co2, co, nh3 = read_sensors()
    if temp is not None:
        print("Temp:", temp, "Hum:", hum, "| CO2:", co2, "CO:", co, "NH3:", nh3)
        display(temp, hum, co2, co, nh3)
    else:
        oled.fill(0)
        oled.text("Sensor Error", 0, 20)
        oled.show()
    time.sleep(5)