#! /usr/bin/env python3

import pigpio
import time
import signal
import sys

pi = pigpio.pi()

PWM_FREQ = 25000        # 25kHZ

FAN_PIN = 18            # BCM pin used to drive PWM fan
WAIT_TIME = 1           # [s] Time to wait between each refresh

OFF_TEMP = 40           # [°C] temperature below which to stop the fan
MIN_TEMP = 45           # [°C] temperature above which to start the fan
MAX_TEMP = 70           # [°C] temperature at which to operate at max fan speed
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)


def getCpuTemperature ():
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
                return float(f.read()) / 1000

def controlFan(frequency):
        pi.hardware_PWM(FAN_PIN, PWM_FREQ, frequency )


def handleFanSpeed(temperature):
        if temperature >= MAX_TEMP:
                controlFan(FAN_HIGH * 10000)
        elif temperature >= MIN_TEMP:
                delta = temperature - MIN_TEMP
                fanspeed = int(FAN_LOW * 10000 + delta * FAN_GAIN * 10000)
                controlFan(fanspeed)
        elif temperature < OFF_TEMP:
                controlFan(FAN_OFF)

try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    while True:
        handleFanSpeed(getCpuTemperature())
        time.sleep(WAIT_TIME)


except KeyboardInterrupt:
        controlFan(FAN_HIGH *  10000)
        pi.stop()

    
