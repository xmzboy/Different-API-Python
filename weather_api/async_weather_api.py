import grequests
import requests
import json
from tkinter import *
from tkinter.ttk import Combobox
import emoji

from rec_data import record_data
from connections import one_connect, get_responses_lst
from constants import WEATHER_STATUS
from messages import get_manual, show_mb, show_err
from log_decorator import log_dec

# @log_dec
# def add_random_places(count):
#     for i in range(count):
#         places.append((uniform(-90, 90), uniform(-180, 180)))


def show_result(show_dct):
    """Show the weather information in text block"""
    try:
        txt.delete(1.0, END)
        try:
            weather = WEATHER_STATUS[show_dct['weather'][0]['main']]
        except Exception as ex:
            print(ex)
            weather = show_dct['weather'][0]['main']
        txt.insert(INSERT, f"{emoji.emojize(':globe_showing_Americas:')}Location: {show_dct['name']},"
                           f" {show_dct['sys']['country']}\n"
                           f"{emoji.emojize(':seedling:')}Weather: {weather}\n"
                           f"{emoji.emojize(':fire:')}Temperature: {round(show_dct['main']['temp'] - 273)}\n"
                           f"{emoji.emojize(':fallen_leaf:')}Feels like: {round(show_dct['main']['feels_like']-273)}\n"
                           f"{emoji.emojize(':droplet:')}Humidity: {round(show_dct['main']['humidity'])}\n"
                           f"{emoji.emojize(':cyclone:')}Wind speed: {show_dct['wind']['speed']}\n"
                           f"{emoji.emojize(':globe_with_meridians:')}Coordinates: {round(show_dct['coord']['lat'],2)},"
                           f" {round(show_dct['coord']['lon'], 2)}")
    except Exception as ex:
        print(ex)
        txt.delete(1.0, END)
        if show_dct['name'] == 'Timeout':
            txt.insert(INSERT, f"Server is not available")
        else:
            txt.insert(INSERT, f"Information is absent")


def record_new_place():
    """Add new place in list"""
    new_places.append((str(lats_entry.get()), str(lons_entry.get())))
    for rec_dct in cache:
        if rec_dct['coord']['lon'] == int(lons_entry.get()) and rec_dct['coord']['lat'] == int(lats_entry.get()):
            places_name.append(rec_dct['name'])
            good_place.append(rec_dct)
    combo['values'] = places_name
    show_mb('saved')


def callback_combo(event):
    """List callback"""
    show_result(good_place[int(combo['values'].index(combo.get()))])


@log_dec
def set_coord():
    """Setting place coordinates"""
    set_dct = one_connect(str(lats_entry.get()), str(lons_entry.get()))
    cache.append(set_dct)
    show_result(set_dct)


def recording_data():
    """Recording data into csv format"""
    record_data(lst[2])
    record_data(lst[5])


class NotFoundAPlace(Exception):
    """Place is not found"""


def delete_place():
    """Delete place from list"""
    try:
        del_place = combo.get()
        places_with_names = dict(zip(places_name, new_places))
        i = 0
        for pl in places_with_names:
            if pl == del_place:
                del new_places[i]
                del places_name[i]
                del good_place[i]
                combo['values'] = places_name
                break
            i += 1
        else:
            raise NotFoundAPlace('The place is not found')
    except Exception as ex:
        show_err(ex)
    else:
        show_mb('deleted')


def settings():
    """The settings window"""
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry('220x200')
    settings_window.resizable(width=False, height=False)

    lbl1 = Label(settings_window, text='     ', font=("Arial Bold", 20))
    lbl1.grid(row=0, column=0)

    manual_button = Button(settings_window, text="     Manual    ", command=get_manual, font=("Arial Bold", 14))
    manual_button.grid(row=0, column=1, sticky=W+E, pady=10)

    add_new_button = Button(settings_window, text="  Add place  ", command=record_new_place, font=("Arial Bold", 14))
    add_new_button.grid(row=2, column=1, sticky=W+E, pady=10)

    delete_button = Button(settings_window, text="Delete place", command=delete_place, font=("Arial Bold", 14))
    delete_button.grid(row=5, column=1, sticky=W+E, pady=10)


cache, places_name, good_place = [], [], []
with open('places.txt') as f:
    places = eval(f.read())
    new_places = []
    new_places.extend(places)

lst = get_responses_lst(places)

for dct in lst:
    if 'country' in dct['sys']:
        if dct['name'] not in places_name:
            places_name.append(dct['name'])
            good_place.append(dct)

recording_data()

window = Tk()
window.title("Weather Here")
window.geometry('400x400')
window.resizable(width=False, height=False)

lbl = Label(window, text='', font=("Arial Bold", 2))
lbl.grid(row=0, column=1)

label = Label(text="Choose a place:", font=("Arial Bold", 12))
label.grid(row=1, column=0, sticky=E)

label = Label(text="Or set your own coordinates:", font=("Arial Bold", 12))
label.grid(row=2, column=0, columnspan=3, sticky=W+E)

lats_label = Label(text="Latitude:", font=("Arial Bold", 12))
lats_label.grid(row=3, column=0, sticky=E)

lats_entry = Entry()
lats_entry.grid(row=3, column=1, sticky=W, ipadx=25)
lats_entry.insert(0, '50')

lons_label = Label(text="Longitude:", font=("Arial Bold", 12))
lons_label.grid(row=4, column=0, sticky=E)

lons_entry = Entry()
lons_entry.grid(row=4, column=1, sticky=W, ipadx=25)
lons_entry.insert(0, '0')

txt = Text(window, width=27, height=10, font=("Arial Bold", 16))
txt.grid(row=6, column=0, columnspan=3, padx=20, ipadx=15, sticky=W+E)

combo = Combobox(window)
combo['values'] = places_name
combo.current(0)
combo.grid(row=1, column=1, sticky=W, ipadx=15)
combo.bind("<<ComboboxSelected>>", callback_combo)

settings_button = Button(text=emoji.emojize(':gear:'), command=settings, font=("Arial Bold", 14))
settings_button.grid(row=1, column=2, ipady=2, sticky=W, ipadx=1)

set_but = Button(text="Search", command=set_coord, font=("Arial Bold", 12))
set_but.grid(row=3, column=2, rowspan=2, ipady=2, pady=10, sticky=W)

show_result(good_place[0])

window.mainloop()

with open('places.txt', 'w') as output_file:
    output_file.write(str(new_places))
