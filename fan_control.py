#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

FAN_PIN = 18            # BCM pin used to drive PWM fan
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 25           # [Hz] 25Hz for Noctua PWM control

OFF_TEMP = 40           # [°C] temperature below which to stop the fan
MIN_TEMP = 45           # [°C] temperature above which to start the fan
MAX_TEMP = 70           # [°C] temperature at which to operate at max fan speed
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)


def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000


def handleFanSpeed(fan, temperature):
    if temperature > MIN_TEMP:
        delta = min(temperature, MAX_TEMP) - MIN_TEMP
        fan.start(FAN_LOW + delta * FAN_GAIN)

    elif temperature < OFF_TEMP:
        fan.start(FAN_OFF)


try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    while True:
        handleFanSpeed(fan, getCpuTemperature())
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
