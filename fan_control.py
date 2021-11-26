#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import atexit

FAN_PIN = 18            # BCM pin used to drive PWM fan
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 25           # [Hz] 25Hz for Noctua PWM control

MIN_TEMP = 45
MIN_TEMP_DEAD_BAND = 5
MAX_TEMP = 70
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100

outside_dead_band_higher = True


def getCpuTemperature():
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    temp = float(res)/1000
    return temp


def setFanSpeed(speed):
    fan.start(speed)
    return()


def handleFanSpeed(temperature, outside_dead_band_higher):

    if not outside_dead_band_higher:
        setFanSpeed(FAN_OFF)
        return

    elif outside_dead_band_higher and temperature < MAX_TEMP:
        step = float(FAN_HIGH - FAN_LOW)/float(MAX_TEMP - MIN_TEMP)
        temperature -= MIN_TEMP
        setFanSpeed(FAN_LOW + (round(temperature) * step))
        return

    elif temperature > MAX_TEMP:
        setFanSpeed(FAN_MAX)
        return
    else:
        return


def handleDeadZone(temperature):
    if temperature > (MIN_TEMP + MIN_TEMP_DEAD_BAND/2):
        return True
    elif temperature < (MIN_TEMP - MIN_TEMP_DEAD_BAND/2):
        return False


def resetFan():
    GPIO.cleanup()  # resets all GPIO ports used by this function


try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    while True:
        temp = float(getCpuTemperature())
        outside_dead_band_higher = handleDeadZone(temp)
        handleFanSpeed(temp, outside_dead_band_higher)
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    resetFan()

atexit.register(resetFan)
