import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        # TODO START
        # send temperature to the cloud service with regular intervals

        while True:

            logging.info(f"Sensor Client {self.did} {self.measurement.get_temperature()}")

            url = common.BASE_URL + f"sensor/{self.did}/current"

            payload = self.measurement.to_json();

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

        # TODO END

    def run(self):

        # TODO START

        # create and start thread simulating physical temperature sensor
        sensor_thread = threading.Thread(target=self.simulator)
        sensor_thread.start()

        # create and start thread sending temperature to the cloud service
        client_thread = threading.Thread(target=self.client)
        client_thread.start()

        # TODO END

