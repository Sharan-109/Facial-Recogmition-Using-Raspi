# Raspberry Pi Smart Gate Security System
# Final Version with Hardware Optimizations

import cv2
import os
import pickle
import time
import numpy as np
import logging
from picamera2 import Picamera2
from gpiozero import AngularServo, DigitalOutputDevice, Button
from gpiozero.pins.pigpio import PiGPIOFactory  # Hardware PWM
from BlynkLib import Blynk
from RPLCD.i2c import CharLCD
import face_recognition
from datetime import datetime

# ========================
# CONFIGURATION
# ========================
# Reduce libcamera logging
logging.getLogger("libcamera").setLevel(logging.WARNING)

I2C_ADDR = 0x27        # Confirm with i2cdetect -y 1
LCD_COLS = 16
LCD_ROWS = 2

# Use hardware PWM for servo
SERVO_PIN = 14         
SERVO_OPEN_ANGLE = 85  # Slightly less than 90 to prevent strain
SERVO_CLOSE_ANGLE = -85

# Keypad configuration
KEYPAD_ROWS = [17, 18, 27, 22]
KEYPAD_COLS = [25, 12, 13, 26]
KEYPAD_LAYOUT = [
    '1', '2', '3', 'A',
    '4', '5', '6', 'B',
    '7', '8', '9', 'C',
    '*', '0', '#', 'D'
]

BLYNK_AUTH = "YOUR_BLYNK_TOKEN"
AUTHORIZED_USERS = ["admin"]
SECRET_PIN = "1337"
MAX_ATTEMPTS = 3
GATE_OPEN_TIME = 5

# ========================
# HARDWARE INITIALIZATION
# ========================
def init_hardware():
    global servo, lcd, rows, cols, picam2
    
    try:
        # Use hardware PWM through pigpio
        factory = PiGPIOFactory()
        servo = AngularServo(SERVO_PIN,
                            min_angle=SERVO_CLOSE_ANGLE,
                            max_angle=SERVO_OPEN_ANGLE,
                            pin_factory=factory)
        
        # Initialize LCD
        lcd = CharLCD(i2c_expander='PCF8574',
                     address=I2C_ADDR,
                     port=1,
                     cols=LCD_COLS,
                     rows=LCD_ROWS)
        lcd.backlight_enabled = True
        lcd.clear()
        
        # Keypad
        rows = [DigitalOutputDevice(pin) for pin in KEYPAD_ROWS]
        cols = [Button(pin, pull_up=False) for pin in KEYPAD_COLS]
        
        # Camera
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"format": 'XRGB8888', "size": (640, 480)},
            controls={"FrameDurationLimits": (33333, 33333)}  # 30fps
        )
        picam2.configure(config)
        return True
        
    except Exception as e:
        logging.error(f"Hardware init failed: {str(e)}")
        return False

# ========================
# CORE FUNCTIONS (remain mostly the same)
# ... [Keep previous core functions unchanged] ...

# ========================
# MAIN SYSTEM WITH IMPROVED ERROR HANDLING
# ========================
def main():
    if not init_hardware():
        print("Critical hardware failure. Check connections.")
        return
    
    # Load face encodings
    try:
        with open("encodings.pickle", "rb") as f:
            data = pickle.loads(f.read())
            known_encodings = data["encodings"]
            known_names = data["names"]
    except FileNotFoundError:
        logging.error("Face encodings not found. Run training first.")
        return

    # Initialize Blynk with connection handler
    blynk = Blynk(BLYNK_AUTH,
                 connect_callback=lambda: print("Blynk connected"),
                 disconnect_callback=lambda: print("Blynk disconnected"))
    
    try:
        picam2.start()
        control_gate("close")
        lcd_show("System Ready", "Scan Face")
        
        while True:
            # Main logic remains the same
            # ...
            
            # Add periodic Blynk sync
            blynk.run()
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        control_gate("close")
        picam2.stop()
        if lcd:
            lcd.clear()
        GPIO.cleanup()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    main()