import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # TODO START
        # send request to cloud service with regular intervals to obtain actuator state

        url = common.BASE_URL + f"actuator/{self.did}/current"

        payload = {}
        headers = {}

        while True:

            response = requests.request("GET", url, headers=headers, data=payload)

            self.state = ActuatorState.from_json(response.text)

            logging.info(f"Actuator Client {self.did} {self.state.state}")
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

        # TODO END

    def run(self):

        # TODO START

        # start thread simulating physical light bulb
        sensor_thread = threading.Thread(target=self.simulator)
        sensor_thread.start()

        # start thread receiving state from the cloud
        client_thread = threading.Thread(target=self.client)
        client_thread.start()

        # TODO END


