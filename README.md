#  Low-Cost 3D Mapping System Using a Single Ultrasonic Sensor

> A LiDAR-inspired 3D spatial mapping system built from scratch using an ultrasonic sensor, custom pan-tilt mechanism, and Python-based point cloud visualization — at a fraction of LiDAR cost.

---


---

##  The Problem

3D spatial mapping typically requires LiDAR modules costing ₹15,000–₹1,50,000+. For low-budget research and educational applications, this is a major barrier. Additionally, no pre-built pan-tilt scanning mechanism was provided — the entire scanning assembly had to be engineered from scratch.

---

##  Our Solution

A two-axis scanning system using two SG90 servo motors driving an HC-SR04 ultrasonic sensor across configurable yaw and pitch angles. Distance measurements at each angular position are converted to 3D Cartesian coordinates and visualized as a real-time point cloud on a PC.

---
##  Hardware Architecture

| Component | Purpose |
|---|---|
| HC-SR04 Ultrasonic Sensor | Distance measurement via 40kHz time-of-flight |
| Arduino Uno | Control, timing, and serial communication |
| SG90 Servo #1 (Base) | Yaw rotation — left/right sweep |
| SG90 Servo #2 (Top) | Pitch rotation — up/down tilt |
| Custom Pan-Tilt Frame | Mechanically assembled two-axis scanning mount |
| Breadboard + Power Rails | Signal distribution and 5V regulation |

---

##  Working Principle

### Distance Measurement
```
Arduino sends 10μs TRIG pulse
        ↓
HC-SR04 emits 8-pulse 40kHz ultrasonic burst
        ↓
Echo returns → Arduino measures pulse width
        ↓
Distance = (pulse_width × speed_of_sound) / 2
         = (time × 343 m/s) / 2
```

### Two-Axis Scanning
The sensor sweeps across a configurable angular grid:
- **Yaw (θ):** Horizontal rotation via base servo
- **Pitch (φ):** Vertical tilt via top servo

At each (θ, φ) position, a distance measurement `d` is taken.

### Coordinate Transformation
Polar → Cartesian conversion for 3D point cloud generation:

```
x = d · cos(φ) · cos(θ)
y = d · cos(φ) · sin(θ)
z = d · sin(φ)
```

Each valid (x, y, z) point is transmitted via serial to a PC for visualization.

---

##  Software Stack

### Arduino Firmware (`src/scanner.ino`)
- PWM-based servo positioning via `Servo.h`
- Ultrasonic trigger/echo timing with `pulseIn()`
- **8-sample averaging** per angular position to reduce noise
- **Stabilization delay** (500ms) after each servo move before measurement
- Outlier rejection: readings < 2cm or > 400cm discarded
- Serial output format: `theta,phi,distance\n`

### Python Visualization (`visualizer/plot_pointcloud.py`)
- Reads serial stream in real time
- Applies coordinate transformation
- Plots live 3D point cloud using `matplotlib` with `mpl_toolkits.mplot3d`
- Color-mapped by distance for depth perception

---

##  Key Technical Challenges & Solutions

### 1. No Pre-Built Pan-Tilt Mechanism
**Problem:** A scanning mount was not provided — had to be built from scratch.  
**Solution:** Engineered a custom two-axis assembly using two SG90 servos. Servo #2 (pitch) is mounted on the rotating arm of Servo #1 (yaw), creating a stable nested-axis structure. Multiple mechanical iterations were required to achieve alignment between axes.

### 2. Servo Jitter Causing Unstable Readings
**Problem:** Rapid servo movements caused vibrations that corrupted distance measurements — readings varied by 15–30cm at the same position.  
**Solution:** Introduced a 500ms stabilization delay after each servo movement before triggering the ultrasonic pulse. Jitter reduced to < 3cm variance.

### 3. Power Instability from Dual Servo Load
**Problem:** Two servos drawing current simultaneously from Arduino's 5V pin caused voltage drops and occasional resets.  
**Solution:** Optimized scanning sequence to never move both servos simultaneously + improved grounding between servo power return and Arduino GND.

### 4. Ultrasonic Sensor Noise & Measurement Errors
**Problem:** HC-SR04 is sensitive to surface angle and texture — angled surfaces scatter sound, returning no echo or false short readings.  
**Solution:**
- 8-sample rolling average per position
- Reject readings outside valid range (2–400cm)
- Restrict scan to ±60° pitch (beyond this, grazing incidence dominates)

### 5. Limited Angular Resolution
**Problem:** Ultrasonic beam has ~15° cone angle, limiting fine object detection.  
**Solution:** Reduced angular step size to 3° (from default 10°) to increase spatial density of the point cloud, partially compensating for beam spread.

---

##  System Specifications

| Parameter | Value |
|---|---|
| Sensor | HC-SR04 (40 kHz ultrasonic) |
| Measurement Range | 2cm – 400cm |
| Angular Resolution (step size) | 3° (configurable) |
| Yaw Range | ±90° (configurable) |
| Pitch Range | ±60° (configurable) |
| Samples per point | 8 (averaged) |
| Scan time (full sweep) | ~4 minutes at 3° steps |
| Output format | 3D point cloud (x, y, z in cm) |

---



---

##  How to Run

**Hardware:**
1. Assemble pan-tilt mechanism with SG90 servos
2. Mount HC-SR04 on top servo arm
3. Connect to Arduino Uno per circuit diagram
4. Power via USB

**Firmware:**
```bash
# Open src/scanner.ino in Arduino IDE
# Select board: Arduino Uno
# Upload to board
```

**Visualization:**
```bash
pip install pyserial matplotlib numpy
python visualizer/plot_pointcloud.py --port COM3 --baud 9600
# Change COM3 to your Arduino's serial port
```

---

##  Future Work

- Replace HC-SR04 with IR sensor array for faster sweep
- Implement SLAM (Simultaneous Localization and Mapping) algorithm
- Real-time ROS integration for robotics applications
- Neural network-based surface reconstruction from sparse point cloud





---

*Built during Year 1 — Birla Institute of Technology - Mesra*
