import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):

    new_state = state.get()

    logging.info(f"Dashboard: {new_state}")

    # TODO: START
    # send HTTP request with new actuator state to cloud service
    url_get = common.BASE_URL + "actuator/" + did + "/current/"
    url_put = common.BASE_URL + "actuator/" + did + "/"
    # get request
    current_state = ActuatorState.from_json(did)
    try:
        response = requests.get(url_get, did)
        response_json = response.json()
        response.raise_for_status()
        print(response_json)
    # If the request fails (404) then print the error.
    except requests.exceptions.HTTPError as error:
        print(error)

    if new_state != current_state:
        #put request
        response = requests.put(url_put, did)
        response_json = response.json()
        response.raise_for_status()
        print(response_json)
        logging.info(f"Dashboard: {new_state}")
    else:
        logging.info(f"Dashboard: {current_state}")


    # TODO: END


def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
