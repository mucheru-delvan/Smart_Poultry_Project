from machine import Pin, I2C
import dht
import time
from i2c_lcd import I2cLcd

# HARDWARE CONFIGURATION
# Sensor
dht_sensor = dht.DHT11(Pin(4))
# If using DHT11 use:
# dht_sensor = dht.DHT11(Pin(4))

# Indicators / Actuators
green  = Pin(7, Pin.OUT)    # SAFE STATE
red    = Pin(5, Pin.OUT)    # HEAT LAMP
blue   = Pin(6, Pin.OUT)    # HUMIDIFIER
white  = Pin(9, Pin.OUT)    # FAN
buzzer = Pin(8, Pin.OUT)    # ALARM

# LCD
i2c = I2C(0, scl=Pin(3), sda=Pin(2), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# SCREEN MANAGER
screen_cycle = 0
last_screen_switch = 0
switch_interval = 3000  # 3 seconds

# MAIN LOOP
while True:
    try:
        # SENSOR READ
        dht_sensor.measure()

        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        print("Temp:", temp, "Hum:", hum)

        # RESET OUTPUTS
        green.off()
        red.off()
        blue.off()
        white.off()
        buzzer.off()

        # NORMAL CONDITION FLAGS
        temp_normal = (24.0 <= temp <= 29.9)
        hum_normal = (65.0 <= hum <= 70.0)

        # DEFAULT LCD TEXT
        temp_line2 = "NORMAL TEMP"
        hum_line2 = "NORMAL HUM"

        # SAFE STATE
        if temp_normal and hum_normal:
            green.on()

        # TEMPERATURE LOGIC
        if temp >= 30.0:
            white.on()      # Fan
            buzzer.on()
            temp_line2 = "TEMP:H FAN:ON"

        elif temp <= 24.0:
            red.on()        # Heat Lamp
            buzzer.on()
            temp_line2 = "TEMP:L LAMP:ON"

        else:
            temp_line2 = "NORMAL TEMP"

        # HUMIDITY LOGIC
        if hum > 70:
            white.on()      # Fan
            buzzer.on()
            hum_line2 = "HUM:H FAN:ON"

        elif hum < 65:
            blue.on()       # Humidifier
            buzzer.on()
            hum_line2 = "HUM:L HMDF:ON"

        else:
            hum_line2 = "NORMAL HUM"

        # SYSTEM STATUS
        if temp_normal and hum_normal:
            status_line2 = "ALL NORMAL"

        elif (temp >= 30.0 and hum < 65) or (temp <= 24.0 and hum > 70):
            status_line2 = "CHECK SYSTEM"

        elif temp >= 30.0 and hum > 70:
            status_line2 = "FAN+ALARM ON"

        elif temp >= 30.0:
            status_line2 = "COOLING ACTV"

        elif temp <= 24.0:
            status_line2 = "HEATING ACTV"

        elif hum < 65:
            status_line2 = "HUMIDIFYING"

        elif hum > 70:
            status_line2 = "VENTILATING"

        else:
            status_line2 = "MONITORING"

        # SCREEN CYCLING TIMER
        current_time = time.ticks_ms()

        if time.ticks_diff(current_time,
                           last_screen_switch) >= switch_interval:

            screen_cycle = (screen_cycle + 1) % 3
            last_screen_switch = current_time

            lcd.clear()

        # SCREEN 1 : TEMPERATURE
        if screen_cycle == 0:

            lcd.hal_write_command(0x80)
            lcd.putstr("TEMP T:{:.1f}C".format(temp))

            lcd.hal_write_command(0xC0)
            lcd.putstr("{:<16}".format(temp_line2))

        # SCREEN 2 : HUMIDITY
        elif screen_cycle == 1:

            lcd.hal_write_command(0x80)
            lcd.putstr("HUM H:{:.0f}%".format(hum))

            lcd.hal_write_command(0xC0)
            lcd.putstr("{:<16}".format(hum_line2))

        # SCREEN 3 : SYSTEM STATUS
        else:

            lcd.hal_write_command(0x80)
            lcd.putstr("SYSTEM STATUS")

            lcd.hal_write_command(0xC0)
            lcd.putstr("{:<16}".format(status_line2))

        time.sleep_ms(200)

    except Exception as e:

        print("Hardware Loop Exception:", e)
        time.sleep(1)