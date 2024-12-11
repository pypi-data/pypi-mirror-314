
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Downloads](https://img.shields.io/pypi/dm/tolmate) ![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue) ![Pre-Release](https://img.shields.io/badge/status-beta-orange)

<!--
![Custom Badge](https://img.shields.io/badge/yourlabel-yourtext-yourcolor) -->

# TolMate

**TolMate** is a Python utility for checking if a value falls within specified tolerance ranges. It provides feedback via console messages and popup windows to alert users about the status of the value, whether it's within range or outside specifications.

---

## Features

- **Tolerance Checks**: Supports up to three (optional) levels of tolerance ranges:

![Tolerances](https://raw.githubusercontent.com/sgiani95/tolmate/refs/heads/main/Bild5.png "Tolerances")

---


  - **Tol 1±**: Normal range (no news, good news)

---

  - **Tol 2±**: Soft warning

<img src="https://raw.githubusercontent.com/sgiani95/tolmate/refs/heads/main/Bild2.png" alt="Soft Warning" title="Soft Warning" style="width:66%;">

---

  - **Tol 3±**: Hard warning

<img src="https://raw.githubusercontent.com/sgiani95/tolmate/refs/heads/main/Bild3.png" alt="Critical Warning" title="Critical Warning" style="width:66%;">

---

  - **Outside tolerances**: Error

  <img src="https://raw.githubusercontent.com/sgiani95/tolmate/refs/heads/main/Bild4.png" alt="Error" title="Error" style="width:66%;">

---

- **Interactive Popups**: Display user-friendly messages with color-coded warnings and action buttons.
- **Dynamic Value Rechecking**: Modify values directly from the popup for re-evaluation.
- **Behavior Configuration**: Enable or disable popups and console messages globally.
- **Simple API**: Easy to integrate into your existing Python projects.
- **Customizable Look**: Highlight alerts with built-in symbols or emojis.
- **Reusable and Lightweight**: Designed to integrate seamlessly into larger projects.

---

## Installation

You can install **TolMate** using pip.

```bash
pip install tolmate
```

## Requirements

- Python 3.x
- `tkinter` (comes pre-installed with Python)

---

## Usage

### Basic Example

```python
from tolmate import configure_behavior, tolmate

# Set global behavior for popups and messages (by default all True)
configure_behavior(show_popup=True, show_message=False)

# Main program example
def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

# Main loop for initial value input
try:
    # Configure global behavior (example: enable both message and popup)
    value = float(input("\nEnter the temperature in degrees Celsius: "))

    if tolmate(value, 20, 30, 10, 50, -10, 80):  # Example ranges
        kelvin = celsius_to_kelvin(value)
        print(f"\nThe temperature in Kelvin is: {kelvin:.2f}")
    else:
        print("\nThe value is outside specifications.")

except ValueError:
    print("Please enter a valid number!")
```