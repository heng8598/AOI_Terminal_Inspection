# AOI Terminal Inspection System

A terminal inspection project using **OpenCV**, **PySide6**, and
**Modbus TCP / UART**.

The system measures terminal **width** and **angle** from a camera
image, communicates with an STM32 board or Modbus TCP relay board,
and provides a simple operator UI.

This is a learning project. Feedback is welcome.



## ✨ Features

- **measurement** —  edge detection on terminal
  width and angle
- **Multi-terminal support** — Ground / Live / Neutral in a single
  inspection pass
- **Multiple working modes**
  - `Manual` — operator clicks to inspect
  - `UART` — triggered by external STM32 board
  - `Modbus TCP` — triggered by IO relay board (IN1 sensor)
  - `Auto` — self-loop continuous inspection

- **Industrial communication**
  - UART (STM32) for event-driven triggering
  - Modbus TCP for relay control (light, air blow / rejection)
- **Complete operator UI** — real-time preview, counter, OK/NG
  history, live result table
- **Robust state machine** — clean flow control with error handling
- **Configurable** — all parameters stored in `config.json`

## 📊 Performance (CPK Report)

Measured on **500 consecutive samples** per terminal.

| Terminal | Metric | Spec (mm / °)       | Mean    | Std     | CPK       | Status |
|----------|--------|---------------------|---------|---------|-----------|--------|
| Ground   | Width  | 4.09 ~ 4.19 ~ 4.29  | 4.1912  | 0.0213  | 1.55      | ✅ OK  |
| Ground   | Angle  | -0.60 ~ 0.00 ~ 0.60 | -0.0121 | 0.0925  | 2.12      | ✅ OK  |
| Live     | Width  | 5.17 ~ 5.27 ~ 5.37  | 5.2707  | 0.0080  | **4.14**  | ✅ OK  |
| Live     | Angle  | 0.50 ~ 1.10 ~ 1.70  | 1.1044  | 0.0458  | **4.34**  | ✅ OK  |
| Neutral  | Width  | 5.18 ~ 5.28 ~ 5.38  | 5.2800  | 0.0085  | 3.94      | ✅ OK  |
| Neutral  | Angle  | -0.60 ~ 0.00 ~ 0.60 | -0.2472 | 0.0594  | 1.98      | ✅ OK  |

**All CPK > 1.33 (process capability threshold).**

## 🛠️ Hardware Requirements

- **Camera**: USB digital microscope (tested with 30 RMB CMOS camera)
  - 640×480 @ 20 fps
  - V4L2-compatible (Linux)
- **Light**: fixed LED  constant current preferred
- **MCU (optional)**: STM32 (UART trigger)
- **Relay board (optional)**: 4-in 4-out relay module with Modbus TCP
  (e.g. PQW_IO_4I_4O_RLY_10A)
- **PC**: any x86_64 with Linux 

---
