import json
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
    url_get = common.BASE_URL + f"actuator/{did}/current/"
    url_put = common.BASE_URL + f"actuator/{did}/"
    #current_state = ActuatorState.from_json(did)
    # get request
    response = requests.get(url_get, did)
    response_json = response.json()
    print(response_json)
    """payload = {'state': 'new_state'}
    update = requests.put(url_put, did, data={payload})
    update_json = ActuatorState.to_json().u"""

    """if new_state != current_state:

        update_json = update.json()
        print(update_json)"""




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
