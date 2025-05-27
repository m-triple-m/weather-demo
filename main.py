import machine
import time
import dht
import ssd1306

# === Pins Setup ===
dht_sensor = dht.DHT11(machine.Pin(2))  # D4
mq135_pin = machine.ADC(0)              # A0
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))  # D1, D2
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Add these constants at the top
R0_CO2 = 100.0  # Resistance in clean air for CO2 (calibrate this)
R0_CO = 100.0   # Resistance in clean air for CO (calibrate this)
R0_NH3 = 100.0  # Resistance in clean air for NH3 (calibrate this)

def calibrate_sensor():
    """Run this in clean air to get R0 values"""
    readings = []
    print("Calibrating... ensure sensor is in clean air")
    for i in range(10):
        raw = mq135_pin.read()
        voltage = (raw / 1024.0) * 3.3
        # Convert to resistance (approximate)
        if voltage > 0:
            resistance = (3.3 - voltage) / voltage * 1000  # Load resistance ~1kΩ
            readings.append(resistance)
        time.sleep(2)
    
    r0 = sum(readings) / len(readings)
    print("Calibrated R0:", r0)
    return r0


def estimate_gases_calibrated(raw):
    voltage = (raw / 1024.0) * 3.3
    
    if voltage <= 0:
        return 400, 10, 10
    
    # Calculate sensor resistance
    rs = (3.3 - voltage) / voltage * 1000  # Assuming 1kΩ load resistor
    
    # Calculate gas concentrations using power law
    # These are approximate - you need datasheet curves for accuracy
    co2 = int(400 * pow(rs/R0_CO2, -2.3))  # Approximate power law
    co = int(10 * pow(rs/R0_CO, -1.5))     # Approximate power law
    nh3 = int(10 * pow(rs/R0_NH3, -1.8))   # Approximate power law
    
    # Clamp values to reasonable ranges
    co2 = max(400, min(10000, co2))
    co = max(10, min(1000, co))
    nh3 = max(10, min(500, nh3))
    
    return co2, co, nh3

def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        gas_raw = mq135_pin.read()
        print("Raw ADC value:", gas_raw)  # Debug line
        co2, co, nh3 = estimate_gases_calibrated(gas_raw)  # Use calibrated version
        return temp, hum, co2, co, nh3
    except Exception as e:
        print("Error:", e)
        return None, None, None, None, None

def display(temp, hum, co2, co, nh3):
    oled.fill(0)
    oled.text("T:{}C  H:{}%".format(temp, hum), 0, 0)
    oled.text("CO2: {} ppm".format(co2), 0, 15)
    oled.text("CO : {} ppm".format(co), 0, 30)
    oled.text("NH3: {} ppm".format(nh3), 0, 45)
    
    # Determine air quality based on CO2 levels
    # These thresholds can be adjusted based on your requirements
    if co2 < 700:
        air_quality = "Good"
    elif co2 < 1000:
        air_quality = "Fair"
    elif co2 < 2000:
        air_quality = "Poor"
    else:
        air_quality = "Bad"
    
    # Add air quality indicator at bottom
    oled.text("Air: {}".format(air_quality), 0, 55)
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