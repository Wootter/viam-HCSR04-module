# HC-SR04 Viam Module Setup Guide

## What's Been Created

A complete Viam module for the HC-SR04 ultrasonic distance sensor with automatic GitHub Actions deployment.

## Files Created

```
HC-SR04/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions for auto-deployment
├── src/
│   ├── __init__.py            # Model registration
│   ├── __main__.py            # Module entry point
│   ├── main.py                # Async startup
│   └── hcsr04.py              # Sensor implementation
├── .gitignore
├── README.md
├── meta.json                   # Viam module metadata
├── requirements.txt            # Python dependencies
└── run.sh                      # Execution script (executable)
```

## Next Steps

### 1. Create GitHub Repository

Go to https://github.com/new and create a new repository named `viam-hcsr04-module`

### 2. Push to GitHub

```powershell
cd "c:\Users\WoutDeelen\Desktop\github\Github Respitories\Viam\HC-SR04"
git remote add origin https://github.com/Wootter/viam-hcsr04-module.git
git branch -M main
git push -u origin main
```

### 3. Add GitHub Secrets

Go to: https://github.com/Wootter/viam-hcsr04-module/settings/secrets/actions

Add these two secrets:
- `VIAM_API_KEY_ID` - Your Viam API Key ID
- `VIAM_API_KEY` - Your Viam API Key

### 4. Create and Push a Tag

```powershell
git tag 1.0.0
git push origin 1.0.0
```

This will automatically trigger the GitHub Action to build and deploy version 1.0.0 to Viam!

## Module Configuration in Viam

**Model:** `wootter:sensor:hcsr04`

**Attributes:**
```json
{
  "trig_pin": 23,
  "echo_pin": 24
}
```

## Hardware Connections

- **VCC** → 5V
- **GND** → Ground
- **TRIG** → GPIO 23 (configurable)
- **ECHO** → GPIO 24 (configurable) - **Use voltage divider!** (5V → 3.3V)

## Sensor Readings

```json
{
  "distance_cm": 15.23,
  "distance_inches": 6.00
}
```

## Features

✅ Automatic deployment via GitHub Actions
✅ Distance measurement in cm and inches
✅ Timeout protection
✅ Error handling and logging
✅ GPIO cleanup on shutdown
✅ Configurable trigger and echo pins
