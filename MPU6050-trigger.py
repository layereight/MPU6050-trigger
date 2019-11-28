#!/usr/bin/python
# -*- coding: utf8 -*-

from mpu6050 import mpu6050
from time import sleep
import os
import logging
import logging.config
import subprocess
import json

logging.config.fileConfig(os.path.dirname(__file__) + '/logging.ini')
logging.info("Start")

DEVNULL = open(os.devnull, 'wb')


def volumio_status():
    process = subprocess.Popen(["/usr/local/bin/volumio", "status"], stdout=subprocess.PIPE)
    return json.load(process.stdout)


def next():
    volumio = volumio_status()

    # print(bla['status'])
    if volumio['status'] != "play":
        return
    logging.info("next")
    subprocess.call(['volumio', 'next'], shell=False, stdout=DEVNULL, stderr=DEVNULL)


def prev():
    volumio = volumio_status()
    # print(bla['status'])
    if volumio['status'] != "play":
        return

    logging.info("prev")
    subprocess.call(['volumio', 'previous'], shell=False, stdout=DEVNULL, stderr=DEVNULL)
    subprocess.call(['volumio', 'previous'], shell=False, stdout=DEVNULL, stderr=DEVNULL)


sensor = mpu6050(0x68)

threshold_left = -3.0
threshold_right = 3.0

accel_data = sensor.get_accel_data()
gyro_data = sensor.get_gyro_data()

lastGyroX = gyro_data['x']
lastGyroY = gyro_data['y']
lastGyroZ = gyro_data['z']
lastY = accel_data['y']
lastX = accel_data['x']
# lastY2 = lastY
# lastY3 = lastY2
threshold = 40.0

while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    #temp = sensor.get_temp()



    currentX = accel_data['x']
    # currentY = accel_data['y']
    # currentZ = accel_data['z']

    gyroX = gyro_data['x'] + 12# * gyro_data['x']
    gyroX = gyroX * gyroX
    gyroY = gyro_data['y'] * gyro_data['y']
    gyroZ = gyro_data['z'] + 1.7

    # currentY = currentY * currentY * currentY + currentY * currentY

    # deltaY = currentY - lastY
    # deltaY2 = lastY - lastY2
    # deltaY3 = lastY2 - lastY3

    # print("ly3: " + str(lastY3))
    # print("ly2: " + str(lastY2))
    # print(" ly: " + str(lastY))
    # print("  y: " + str(currentY))
    # print("  x: " + str(currentX))
    # print("dy3: " + str(deltaY3))
    # print("dy2: " + str(deltaY2))
    # print(" dy: " + str(deltaY))



    # sum = currentX + currentY + currentZ



    # event = ""

    # if deltaY < threshold_left and deltaY2 < threshold_left and deltaY3 < threshold_left:
    #     event = "left"
    # elif deltaY > threshold_right and deltaY2 > threshold_right and deltaY3 > threshold_right:
    #     event = "right"

    # if -1.0 > currentY:
    #     event = "left"
    # elif 1.0 < currentY:
    #     event = "right"

    # if gyroZ > threshold and lastGyroZ < threshold and gyroY < 120 and gyroX < 120:
    if currentX < threshold_left and lastX > threshold_left and gyroX < 120:# and gyroX < 120:
        event = "left"
        prev()
    # elif gyroZ < -threshold and lastGyroZ > -threshold and gyroY < 120 and gyroX < 120:
    elif currentX > threshold_right and lastX < threshold_right and gyroX < 120:# and gyroX < 120:
        event = "right"
        next()
    #
    # lastGyroX = gyroX
    # lastGyroY = gyroY
    lastGyroZ = gyroZ


    # print("x: " + str(currentX))
    # print("y: " + str(currentY) + " " + event)
    # print("")
    # print("z: " + str(accel_data['z']))
    # print("sum: " + str(sum))
    # print("  e: " + event)


    # lastY3 = lastY2
    # lastY2 = lastY
    # lastY = currentY
    lastX = currentX

    # print("\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F")

    # print("Accelerometer data")
    # print("x: " + str(accel_data['x']))
    # print("y: " + str(currentY))
    # print("z: " + str(accel_data['z']))
    #
    #
    # print("Gyroscope data")
    # print("gyro x: " + str(gyroX))
    # print("gyro y: " + str(gyroY))
    # print("gyro z: " + str(gyroZ) + " " + event)


    # print("")

    #    print("Temp: " + str(temp) + " C")
    sleep(0.1)
