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

        # TODO: START
        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response
        while True:
            payload = {'state': 'new state'}
            r = requests.get(common.BASE_URL + f"actuator/{self.did}/current/", payload)
            response_json = r.json()
            new_state = response_json['state']
            u = requests.put(common.BASE_URL + f"actuator/{self.did}/")
            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):

        pass
        # TODO: START

        # start thread simulating physical light bulb
        logging.info(f"Actuator {self.did} starting")

        time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)
        # start thread receiving state from the cloud

        # TODO: END


