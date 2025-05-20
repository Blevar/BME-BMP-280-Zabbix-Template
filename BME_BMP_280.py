#!/usr/bin/env python3

import sys
import board
import busio

from adafruit_bmp280 import Adafruit_BMP280_I2C
from adafruit_bme280 import basic as adafruit_bme280

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Wait for I2C bus
while not i2c.try_lock():
    pass

chip_id = None

try:
    reg = bytearray([0xD0])
    result = bytearray(1)
    i2c.writeto_then_readfrom(0x76, reg, result)
    chip_id = result[0]
finally:
    i2c.unlock()

sensor = None
sensor_type = None

try:
    if chip_id == 0x60:
        sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
        sensor_type = "BME280"
    elif chip_id == 0x58:
        sensor = Adafruit_BMP280_I2C(i2c, address=0x76)
        sensor_type = "BMP280"
    else:
        print("Unknown sensor or chip ID: 0x%02X" % chip_id)
        sys.exit(1)

    print(f"Sensor: {sensor_type}")
    print("Temperature: %.1f C" % sensor.temperature)
    if sensor_type == "BME280":
        print("Humidity: %.1f %%RH" % sensor.relative_humidity)
    print("Pressure: %.1f hPa" % sensor.pressure)

except Exception as e:
    print("Error:", e)
    sys.exit(2)
