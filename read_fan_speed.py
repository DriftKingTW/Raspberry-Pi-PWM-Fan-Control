#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# Pin configuration
TACH = 24       # Fan's tachometer output pin
PULSE = 2       # Noctua fans puts out two pluses per revolution
WAIT_TIME = 1   # [s] Time to wait between each refresh

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TACH, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull up to 3.3V

# Setup variables
t = time.time()
rpm = 0


# Caculate pulse frequency and RPM
def fell(n):
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.005:
        return  # Reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / PULSE) * 60
    t = time.time()


# Add event to detect
GPIO.add_event_detect(TACH, GPIO.FALLING, fell)

try:
    while True:
        print("%.f RPM" % rpm)
        rpm = 0
        time.sleep(1)   # Detect every second

except KeyboardInterrupt:   # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()          # resets all GPIO ports used by this function
