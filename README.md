# 👻 Skull Tracker Project

A motion-tracking system powered by **Raspberry Pi** and **Arduino**, communicating over **NRF24L01** radios.  
The goal is to detect visitor distance, calculate the necessary tracking angle, and drive motors to create responsive, lifelike movement.

---

## ✅ What Works

### 🥧 Raspberry Pi
- ✅ Sending numerical data over radio  
- ✅ Reading distance from sensors  

### 🔧 Arduino
- ✅ Receiving transmitted numbers  
- ✅ Calculating target angle based on input  

---

## 🚧 To Do
- [ ] Measure to the center of the walkway  
- [ ] Calculate the required turn angle  
- [ ] Drive motor to reach the desired angle  
- [ ] Reset skulls to a neutral position when distance exceeds a threshold  
- [ ] Assign node numbers  
  - Odd = Left  
  - Even = Right  

---

## 🧠 Overview
This project combines **RF communication**, **sensor input**, and **motor control** to create synchronized reactive movement across multiple Arduino-controlled nodes — perfect for animatronics, interactive displays, or Halloween setups.

---

## ⚙️ Tech Stack
- **Hardware:** Raspberry Pi, Arduino Uno, NRF24L01 radios, Ultrasonic sensors, Stepper motors  
- **Languages:** Python, C++ (Arduino)  

---

> _“If it moves, it lives.”_ — Project Motto
