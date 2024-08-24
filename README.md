# Home-Energy-Monitor

## Overview
This project is an open-source energy monitoring solution designed to track and measure power consumption in a household. The design is centered around the Raspberry Pi Pico W, interfaced with Current Transformer (CT) sensors via a custom PCB. The project is developed using KiCad for PCB design and is part of an open-source hardware (OSH) initiative.

![image](/Hardware/pcb-render.png)

## Features
1. Real-time power monitoring: Accurately measure and track power usage in real-time using CT sensors.
2. Wireless communication: The RPi Pico W provides wireless connectivity, enabling easy integration with IoT platforms.
3. Scalable design: Supports multiple CT sensors to monitor different circuits or devices.
4. Open-source hardware and software: The design files and source code are freely available for customization and improvement as part of the OSH initiative.

![image](/Hardware/powertiger-case.jpg)

## Project Components
* Raspberry Pi Pico W: The microcontroller at the heart of the project, providing processing power and wireless connectivity.
* Custom PCB: Designed in KiCad, this PCB interfaces with the CT sensors for power measurement of various terminals.
* CT Sensors: Used to measure the current flowing through the electrical wires, providing the data needed for power calculation.
* Software: The firmware is written in CircuitPython, running on the RPi Pico W.

| | Components | Count |
|-|------------|-------|
|1| SCT-013-030 | 5 |
|2| SCT-013-015 | 5 |
|3| SCT-013-005 | 6 |

The json config support configuring 16 CT sensors in any combination as required.

## Grafana Dashboard

![image](/Grafana/PowerTiger-Grafana-Dashboard.png)

