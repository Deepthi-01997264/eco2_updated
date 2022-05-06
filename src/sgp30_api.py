# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import time
import board
import busio
import adafruit_sgp30
from datetime import datetime
import json
import os
from src.mail import send_message

def get_info(mail_server,new_sheet_instance,timer,limit,from_email,to_email,json_baseline_eCO2,json_baseline_TVOC):
    timer = timer if timer else 300
    limit = limit if limit else 1000
    to_email = to_email if to_email else "jeomansang@gmail.com"

    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

    # Create library object on our I2C port
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

    print("SGP30 serial #", [hex(i) for i in sgp30.serial])

    sgp30.iaq_init()
    baseline_eCO2 = sgp30.baseline_eCO2
    baseline_TVOC = sgp30.baseline_TVOC
    
    if baseline_eCO2 == 0 or baseline_eCO2 == None:
        if json_baseline_eCO2 == "" or json_baseline_eCO2 == 0:
            json_baseline_eCO2 = 0x8973
            json_baseline_TVOC = 0x8AAE
        sgp30.set_iaq_baseline(json_baseline_eCO2, json_baseline_TVOC)
        json_dict = {"eco2":json_baseline_eCO2,"tvoc":json_baseline_TVOC}
    else:
        json_dict = {"eco2":baseline_eCO2,"tvoc":baseline_TVOC}
    with open(os.path.join(os.path.dirname(__file__),"baseline_values.json"), 'w') as fp:
        json.dump(json_dict, fp)
    elapsed_sec = 0
    start_time = datetime.now()
    while True:
        print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
        time.sleep(1)
        elapsed_sec += 1
        if elapsed_sec > 10:
            elapsed_sec = 0
            print(
                "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
            )
            json_dict = {"eco2":sgp30.baseline_eCO2,"tvoc":sgp30.baseline_TVOC}
            with open(os.path.join(os.path.dirname(__file__),"baseline_values.json"), 'w') as fp:
                json.dump(json_dict, fp)
        end_time = datetime.now()
        delta_time = end_time - start_time
        if  int(delta_time.total_seconds()) >= int(timer):
            new_sheet_instance.append_row([end_time.strftime("%H:%M:%S"),sgp30.eCO2])
            start_time = end_time
            if int(sgp30.eCO2) >= int(limit):
                print('hello')
                send_message(mail_server,from_email,to_email,"\nSUBJECT : CO2 LEVEL NOTIFICATION. Currently is at {} ppm.".format(sgp30.eCO2))
