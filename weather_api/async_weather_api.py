import grequests
import requests
import json
from tkinter import *
from random import uniform
import time

from log_decorator import log_dec
import gui


@log_dec
def add_random_places(count, places):
    for i in range(count):
        places.append((uniform(-90, 90), uniform(-180, 180)))


# add_random_places(1, places)

window = Tk()
start = time.time()
gui.start_program(window)
window.mainloop()
print(time.time() - start)
