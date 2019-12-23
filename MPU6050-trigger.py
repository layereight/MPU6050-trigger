#!/usr/bin/env python3
# -*- coding: utf8 -*-

from mpu6050 import mpu6050
import time
import os
import logging
import logging.config
import subprocess
import json
from enum import Enum, unique

logging.config.fileConfig(os.path.dirname(__file__) + '/logging.ini')
logging.info("Start")


@unique
class AccelCalibration(Enum):
    X = -0.375
    Y = -0.25
    Z = 9.3


THRESHOLD_X_FORWARD = AccelCalibration.X.value - 3.5
THRESHOLD_X_BACK = AccelCalibration.X.value + 3.5

TOLERANCE_Y = 0.45

MIN_Y = AccelCalibration.Y.value - TOLERANCE_Y
MAX_Y = AccelCalibration.Y.value + TOLERANCE_Y


MIN_Z = 0
MAX_Z = AccelCalibration.Z.value - 1.0


def volumio_status():
    process = subprocess.Popen(["/usr/local/bin/volumio", "status"], stdout=subprocess.PIPE)
    return json.loads(str(process.stdout.read(), "utf-8"))


def next():
    logging.info("next")
    volumio = volumio_status()
    if volumio['status'] != "play":
        return
    subprocess.call(['volumio', 'next'], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def prev():
    logging.info("prev")
    volumio = volumio_status()
    if volumio['status'] != "play":
        return
    subprocess.call(['volumio', 'previous'], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(['volumio', 'previous'], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def in_range(value, min, max):
    return min < value < max


def log_raw_data(accel_data, gyro_data = None, temp = None):
    logging.debug("Accelerometer data")
    logging.debug("x: " + str(accel_data["x"]))
    logging.debug("y: " + str(accel_data["y"]) + "[" + str(MIN_Y) + ", " + str(MAX_Y) + "]")
    logging.debug("z: " + str(accel_data["z"]) + "[" + str(MIN_Z) + ", " + str(MAX_Z) + "]")
    if gyro_data is not None:
        logging.debug("Gyroscope data")
        logging.debug("gyro x: " + str(gyro_data["x"]))
        logging.debug("gyro y: " + str(gyro_data["y"]))
        logging.debug("gyro z: " + str(gyro_data["z"]))
    if temp is not None:
        logging.debug("Temp: " + str(temp) + " C")


sensor = mpu6050(0x68)

accel_data = sensor.get_accel_data()
lastX = accel_data['x']
lastY = accel_data['y']
lastZ = accel_data['z']

while True:
    accel_data = sensor.get_accel_data()
    # gyro_data = sensor.get_gyro_data()
    # temp = sensor.get_temp()

    currentX = accel_data['x']
    currentY = accel_data['y']
    currentZ = accel_data['z']

    log_raw_data(accel_data)
    # log_raw_data(accel_data, gyro_data, temp)

    if in_range(THRESHOLD_X_FORWARD, currentX, lastX) and in_range(currentY, MIN_Y, MAX_Y) and in_range(currentZ, MIN_Z, MAX_Z):
        prev()
    elif in_range(THRESHOLD_X_BACK, lastX, currentX) and in_range(currentY, MIN_Y, MAX_Y) and in_range(currentZ, MIN_Z, MAX_Z):
        next()

    lastX = currentX
    lastY = currentY
    lastZ = currentZ

    time.sleep(0.1)
