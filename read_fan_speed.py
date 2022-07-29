#!/usr/bin/python
# -*- coding: utf-8 -*-
import pigpio
pi = pigpio.pi()

import time

# Pin configuration
TACH = 24       # Fan's tachometer output pin
PULSE = 2       # Noctua fans puts out two pluses per revolution
WAIT_TIME = 15   # [s] Time to wait between each refresh


# Setup variables
t = time.time()
rpm = 0


# Caculate pulse frequency and RPM
def fell(m,n,o):
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.002:
        return  # Reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / PULSE) * 60
    t = time.time()


# Add event to detect
pi.callback(TACH, pigpio.FALLING_EDGE, fell)

try:
    while True:
        print("%.f RPM" % rpm)
        rpm = 0
        time.sleep(WAIT_TIME)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    pi.clear_bank_1(TACH) # Reset TACH-Pin
