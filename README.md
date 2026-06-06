# Smart Environmental Monitoring and Control System for Poultry Farming

An automated, climate-control prototyping system engineered for intelligent poultry environments. Built with **MicroPython** on the **ESP32-C3** platform, this system dynamically tracks humidity and temperature fluctuations using a DHT sensor, parsing real-time data via a cycled LCD dashboard alongside visual and audible diagnostic alert nodes.

## 🚀 Features
* **Tri-Screen Information Carousel:** Rotates dynamically every 3 seconds to display distinct Temperature Status, Humidity Status, and overall System Status screens.
* **Intelligent Logic Parsing:** Accurately detects and warns users against conflicting environmental loops (e.g., Cold + High Humidity) using specialized `CHECK SYSTEM` alerts.
* **Simulated Actuator Array:** Uses specialized safe-voltage LED arrays to simulate industrial ventilation fans, heat lamps, and humidifiers without physical motor overhead.

## ⚙️ Functional System Logic
The system continuously monitors climate metrics and automatically triggers the following states:

* **Everything is Normal** (Temp: 20.0–29.9°C | Hum: 40–70%): Green LED turns ON/blinks. LCD displays `NORMAL TEMP`, `NORMAL HUM`, and `ALL NORMAL`.
* **High Temperature** (Temp ≥ 30°C): White LED (Fan) and Buzzer turn ON. LCD displays `TEMP FAN` and `COOLING ACTV`.
* **Low Temperature** (Temp ≤ 19.9°C): Red LED (Heat Lamp) and Buzzer turn ON. LCD displays `TEMP LAMP` and `HEATING ACTV`.
* **High Humidity** (Hum > 70%): White LED (Fan) and Buzzer turn ON. LCD displays `HUM FAN` and `VENTILATING`.
* **Low Humidity** (Hum < 40%): Blue LED (Humidifier) and Buzzer turn ON. LCD displays `HUM HMDF` and `HUMIDIFYING`.
* **High Temp & High Hum**: White LED (Fan) and Buzzer turn ON. LCD displays `FAN+ALARM ON`.
* **Conflicting States** (High Temp + Low Hum OR Low Temp + High Hum): Relevant indicators and Buzzer turn ON. LCD flags a critical `CHECK SYSTEM` warning.

## 🛠️ Circuit Composition & Pinout
| Component | ESP32-C3 Pin | Function / Simulation Mapping |
| :--- | :--- | :--- |
| **DHT Sensor** | GPIO 2 | Environmental Climate Input |
| **Buzzer** | GPIO 3 | Audio Alarm Node |
| **Red LED** | GPIO 4 | Heat Lamp Indicator |
| **Blue LED** | GPIO 5 | Humidifier Indicator |
| **Green LED** | GPIO 6 | System Status Normal Indicator |
| **White LED** | GPIO 7 | Ventilation Fan Indicator |
| **I2C LCD (16x2)**| GPIO 8 (SDA), GPIO 9 (SCL) | 3-Second Information Carousel Bus |

## 💻 How to Run the Simulation
This project is designed and fully benchmarked directly inside the **Wokwi** simulation engine.
1. Open the repository files inside the `src/` directory.
2. Map your virtual environment wiring according to the pinout matrix above.
3. Boot the environment runtime setup inside your web browser.

## 📈 Future Scalability & Upgrades
* **Industrial Actuators:** Swapping the indicator LEDs out for physical relay modules to switch actual 220V AC extraction fans and physical heat lamps.
* **IoT Cloud Integration:** Utilizing the ESP32-C3's native Wi-Fi capabilities to feed live telemetry data to a remote web dashboard or mobile app.
* **SMS Notifications:** Integrating a hardware GSM module to broadcast text alerts to the farmer immediately during a `CHECK SYSTEM` event.
