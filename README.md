# Thermal Derating Controller for an EV Drive (Simulation)

## 1. Overview
This project simulates an Arduino-based controller that monitors component
temperature and automatically reduces or cuts off drive power to prevent
overheating. This is the same idea as **thermal derating**, which is used to
protect batteries and motors in electric vehicle powertrains.

> **Note:** This is a **simulation only**, built in Wokwi. No physical hardware
> was built. The LED represents the drive motor: its brightness shows the PWM
> drive output.

**Live simulation:** https://wokwi.com/projects/481077720144435201

## 2. Objectives
- Read temperature from a sensor and decide the allowed drive output
- Reduce drive power when the temperature is high (derate) and stop it when
  the temperature is too high (cut-off)
- Stop the drive when an obstacle is detected
- Log the simulation data and analyse it with Python
- Check the chosen temperature limits with a simple thermal model

## 3. Components (simulated)
| Component | Purpose | Arduino pin |
|---|---|---|
| Arduino Uno | Main controller | - |
| DS18B20 temperature sensor | Measures battery or motor temperature | D2 (DQ) |
| HC-SR04 ultrasonic sensor | Detects obstacles | D9 (TRIG), D10 (ECHO) |
| LED + 220 Ω resistor | Represents motor speed using PWM | D5 |
| Buzzer | Alerts when the drive is stopped | D8 |

All sensor and component power pins connect to 5V and GND.

## 4. Circuit


Wiring summary:
- DS18B20: VCC to 5V, DQ to D2, GND to GND
- HC-SR04: VCC to 5V, TRIG to D9, ECHO to D10, GND to GND
- Buzzer: + to D8, − to GND
- LED: D5 through the 220 Ω resistor to the LED anode, cathode to GND

## 5. Control logic
| Condition | Drive output (PWM) | State |
|---|---|---|
| Temperature ≤ 60 °C | 100% | NORMAL |
| 60 °C < Temperature ≤ 75 °C | about 58% | DERATE |
| Temperature > 75 °C | 0% (buzzer on) | OVERTEMP_STOP |
| Obstacle closer than 20 cm | 0% (buzzer on) | OBSTACLE_STOP |

The obstacle check overrides the temperature check, so the drive stops
whenever an obstacle is detected.

Limits used in the code:
```cpp
const float TEMP_WARN = 60.0;   // start derating
const float TEMP_CUT  = 75.0;   // cut off drive
const int   OBSTACLE_CM = 20;   // stop distance
```

## 6. Simulation results
The temperature slider on the DS18B20 in Wokwi was moved through different
values to test each state.

| Test | Screenshot |
|---|---|
| Normal (25 °C): LED bright | ![Normal](images/02_normal.png) |
| Derate (65 °C): LED dim | ![Derate](images/03_derate.png) |
| Over-temperature (80 °C): LED off, buzzer on | ![Over-temperature](images/04_overtemp.png) |
| Obstacle under 20 cm: LED off, buzzer on | ![Obstacle](images/05_obstacle.png) |

### Logged data
The Serial Monitor output was saved to `data/log.csv` with these columns:
`time_s, temp_C, distance_cm, speed_pct, state`

### Temperature vs. drive output

The graph shows the drive output dropping when the temperature crosses
60 °C and falling to zero above 75 °C.

## 7. Analytical thermal model
A simple lumped thermal model was used to see how current affects the
temperature of a component:

```
m·cp · dT/dt = I²·R − h·A · (T − T_ambient)
```

| Symbol | Meaning | Value used (assumed) |
|---|---|---|
| m·cp | Thermal mass | 200 J/K |
| R | Electrical resistance | 0.05 Ω |
| h·A | Heat transfer to surroundings | 0.8 W/K |
| T_ambient | Ambient temperature | 25 °C |


Higher current produces much more heat (heat generated grows with I²), so
the temperature rises faster and reaches the derate and cut-off limits sooner.
This supports the use of temperature-based derating.

## 8. Folder structure
```
thermal-derating-controller/
├── wokwi/
│   └── sketch.ino          Arduino code
├── analysis/
│   ├── plot_log.py         Plots temperature vs drive output
│   └── thermal_model.py    Lumped thermal model
├── data/
│   └── log.csv             Simulation log
├── images/                 Circuit, screenshots and graphs
└── README.md
```

## 9. How to run
**Simulation**
1. Open the Wokwi project link above and press **Play**.
2. Click the DS18B20 sensor and move the temperature slider.
3. Click the HC-SR04 sensor and change the distance.
4. Watch the LED, the buzzer and the Serial Monitor output.

**Analysis (Python)**
```bash
pip install pandas matplotlib
python analysis/plot_log.py
python analysis/thermal_model.py
```
Run these commands from the main project folder.

## 10. What I learned
- How thermal derating protects EV batteries and motors
- PWM control and sensor interfacing with Arduino
- Logging simulation data and validating behaviour with Python
- Basic lumped thermal modelling (heat generation and heat loss)

## 11. Limitations
- This is a simulation only, with no real hardware testing
- The temperature is set manually with a slider, not produced by a real
  heating process
- The thermal model uses assumed values, not measured ones
- The LED represents the motor; no real motor or vehicle is modelled

## 12. Future improvements
- Connect the thermal model to the controller so that temperature responds
  to the drive current automatically
- Add a DC motor and motor driver in a simulator that supports them
- Replace fixed limits with a smooth derating curve
- Add a second temperature sensor for the battery and the motor

## 13. Tools used
Arduino (C++), Wokwi, Python (pandas, matplotlib), GitHub

