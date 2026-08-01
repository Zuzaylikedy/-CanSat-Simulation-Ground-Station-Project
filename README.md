#  CanSat Simulation & Ground Station Project
This repository contains the full end-to-end design, flight trajectory analysis, and real-time telemetry ground station software for a standard *CanSat* payload system.

## Overview
The project is structured into three main engineering phases:
 1. *Mechanical & Structural Design (3D CAD):* A modular 3-tier internal chassis, protective outer body tube, and a flexible TPU shock-absorbing base designed in Ansys SpaceClaim.
 2. *Aerodynamic & Flight Simulation:* Flight dynamics, mass properties, and parachute descent rate optimization modeled in OpenRocket.
 3. *Virtual Hardware Testing (Wokwi):* Pre-hardware validation of C++ logic and NMEA-formatted telemetry generation using Arduino Uno R3.
 4. *Telemetry & Ground Station GUI:* A real-time data visualizer built with Python (Tkinter & Matplotlib) featuring a dynamic orientation compass, telemetry status cards, and live altitude plotting.

## System Architecture
### 1. Mechanical Design (Ansys SpaceClaim)
 * *Modular Chassis:* 3-tier internal mounting plates secured via 4$\times$ M3 threaded rods.
 * *Impact Mitigation:* Bottom-mounted TPU (Thermoplastic Polyurethane) damping base.
 * *Dimensions:* Outer diameter tailored to fit standard rocket payload bays (6.8\text{ cm}).
   ![Mekanik görünüş1](docs/images/cansat_1.png)
   ![Mekanik görünüş2](docs/images/cansat_2.png)
   ![Mekanik görünüş3](docs/images/cansat_3.png)
   ![Mekanik görünüş patlamış](docs/images/cansat_exploded.png)
   
### 2. Flight Dynamics & Trajectory (OpenRocket)
 * *Rocket Length:* 75\text{ cm} | *Max Diameter:* 6.8\text{ cm}
 * *Apogee (Peak Altitude):* 543\text{ m} (Target range: 400 - 600\text{ m})
 * *Descent Velocity:* Stable \sim 10\text{ m/s} descent rate under parachute recovery.
 * *Motor Configuration:* G76G-5

### 3. Virtual Hardware Simulation (Wokwi)
Prior to physical assembly, embedded logic was validated virtually on Wokwi:
 * *Microcontroller:* Arduino Uno R3
 * *Protocol:* Serial (UART) streaming using custom NMEA CSV telemetry packets ($CANSAT,PACKET_NO,ALTITUDE,TEMP,HEADING*)
 * *Interactive Simulation Link:* (https://wokwi.com/projects/471048054030254081)
   
### 4. Ground Station Dashboard (Python)
The Ground Station reads NMEA-formatted telemetry data packets ($CANSAT,PACKET_NO,ALTITUDE,TEMP,HEADING*) over Serial/UART and displays:
 * *Live Altitude Tracking:* Real-time descent plot with turbulence noise emulation.
 * *Dynamic Compass Widget:* Custom Canvas-rendered compass needle tracking satellite heading (0-360^\circ).
 * *Telemetry Telemetry Data Card:* Packet counter, temperature, altitude, and orientation angles.
![Yer İstasyonu Arayüzü](docs/images/ground_station_ui.png)

## Tech Stack & Tools
 * *CAD Modeling:* Ansys SpaceClaim 2026
 * *Trajectory Simulation:* OpenRocket
 * *GUI & Plotting:* Python 3.x, tkinter, matplotlib
 * *Communication Protocol:* UART / Serial Data Link (NMEA CSV format)
 * *Embedded Hardware Target:* Arduino Nano / Uno R3 with BMP280 & HMC5883L/GY-271

