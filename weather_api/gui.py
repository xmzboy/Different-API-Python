from tkinter import *
from tkinter.ttk import Combobox
import tkinter.messagebox as mb
from random import uniform
import emoji
from functools import partial

from rec_data import record_data
from log_decorator import log_dec
from connections import one_connect, get_responses_lst
from constants import WEATHER_STATUS


cache = []


def show_result(dct, txt_spot):
    try:
        txt_spot.delete(1.0, END)
        try:
            weather = WEATHER_STATUS[dct['weather'][0]['main']]
        except Exception:
            weather = dct['weather'][0]['main']
        txt_spot.insert(INSERT, f"{emoji.emojize(':globe_showing_Americas:')}Location: {dct['name']},"
                        f" {dct['sys']['country']}\n"
                        f"{emoji.emojize(':seedling:')}Weather: {weather}\n"
                        f"{emoji.emojize(':fire:')}Temperature: {round(dct['main']['temp'] - 273)}\n"
                        f"{emoji.emojize(':fallen_leaf:')}Feels like: {round(dct['main']['feels_like'] - 273)}\n"
                        f"{emoji.emojize(':droplet:')}Humidity: {round(dct['main']['humidity'])}\n"
                        f"{emoji.emojize(':cyclone:')}Wind speed: {dct['wind']['speed']}\n"
                        f"{emoji.emojize(':globe_with_meridians:')}Coordinates: {round(dct['coord']['lat'], 2)},"
                        f" {round(dct['coord']['lon'], 2)}")
    except Exception:
        txt_spot.delete(1.0, END)
        txt_spot.insert(INSERT, f"Information is absent")


def record_new_place(new_places, lats_entry, lons_entry, places_names, good_places, combo):
    new_places.append((str(lats_entry.get()), str(lons_entry.get())))
    for dct in cache:
        if dct['coord']['lon'] == int(lons_entry.get()) and dct['coord']['lat'] == int(lats_entry.get()):
            places_names.append(dct['name'])
            good_places.append(dct)
    combo['values'] = places_names
    mb.showinfo("Information", "Your data has been successfully saved")


def get_manual():
    mb.showinfo("Manual", "Welcome to the Weather API Application Manual!\n"
                          "This application will show you the weather in selected cities or at given coordinates.\n"
                          "To search for information about the weather in one of the cities, select this city in the"
                          "drop-down list. The data itself will appear in the text box below.\n"
                          "To search for weather information by coordinates, enter the latitude of the place you are"
                          "looking for in the 'Latitude' field, and its longitude in the 'Longitude' field. Click on"
                          "the 'Search' button and enjoy the result given in the text field.\n"
                          "To save a place in the drop-down list, enter the coordinates, Click on"
                          "the 'Search' button, next click on the settings button, and then on the 'Add place' button."
                          "If the location has been successfully added, a notification will appear.\n"
                          "To remove a place from the list, select the place from the list and press the 'Delete' button.\n"
                          "If the deletion was successful, a notification will appear.\n"
                          "Restart the program and enjoy the result.")


def callbackFunc(event):
    show_result(good_place[int(combo['values'].index(combo.get()))], txt)


@log_dec
def set_coord(lats_entry, lons_entry, txt):
    dct = one_connect(str(lats_entry.get()), str(lons_entry.get()))
    cache.append(dct)
    show_result(dct, txt)


@log_dec
def add_random_places(count, places):
    for i in range(count):
        places.append((uniform(-90, 90), uniform(-180, 180)))


def recording_data(lst):
    record_data(lst[2])
    record_data(lst[5])


class NotFoundAPlace(Exception):
    """Place is not found"""


def delete_place(combo, places_name, new_places):
    try:
        del_place = combo.get()
        places_with_names = dict(zip(places_name, new_places))
        i = 0
        for pl in places_with_names:
            if pl == del_place:
                del new_places[i]
                del places_name[i]
                combo['values'] = places_name
                break
            i += 1
        else:
            raise NotFoundAPlace('The place is not found')
    except Exception as ex:
        mb.showerror("Error", ex)
    else:
        mb.showinfo("Information", "Your data has been successfully deleted")


def settings(window, combo, places_name, new_places, lats_entry, lons_entry, good_place):
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry('220x200')
    settings_window.resizable(width=False, height=False)

    lbl = Label(settings_window, text='     ', font=("Arial Bold", 20))
    lbl.grid(row=0, column=0)

    manual_button = Button(settings_window, text="     Manual    ", command=get_manual, font=("Arial Bold", 14))
    manual_button.grid(row=0, column=1, sticky=W+E, pady=10)

    add_new_button = Button(settings_window, text="  Add place  ", command=partial(record_new_place, new_places,
                                                                                   lats_entry, lons_entry, places_name,
                                                                                   good_place, combo), font=("Arial Bold", 14))
    add_new_button.grid(row=2, column=1, sticky=W+E, pady=10)

    delete_button = Button(settings_window, text="Delete place", command=partial(delete_place, combo, places_name, new_places), font=("Arial Bold", 14))
    delete_button.grid(row=5, column=1, sticky=W+E, pady=10)

places_name, good_place = [], []


def start_program(window):
    with open('places.txt') as f:
        places = eval(f.read())
        new_places = []
        new_places.extend(places)

    # add_random_places(1, places)
    lst = get_responses_lst(places)

    for dct in lst:
        if 'country' in dct['sys']:
            if dct['name'] not in places_name:
                places_name.append(dct['name'])
                good_place.append(dct)

    recording_data(lst)

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

    global txt
    txt = Text(window, width=27, height=10, font=("Arial Bold", 16))
    txt.grid(row=6, column=0, columnspan=3, padx=20, ipadx=15, sticky=W+E)

    global combo
    combo = Combobox(window)
    combo['values'] = places_name
    combo.current(0)
    combo.grid(row=1, column=1, sticky=W, ipadx=15)
    combo.bind("<<ComboboxSelected>>", callbackFunc)

    settings_button = Button(text=emoji.emojize(':gear:'),
                             command=partial(settings, window, combo, places_name, new_places, lats_entry, lons_entry,
                                             good_place), font=("Arial Bold", 14))
    settings_button.grid(row=1, column=2, ipady=2, sticky=W, ipadx=1)

    set_but = Button(text="Search", command=partial(set_coord, lats_entry, lons_entry, txt), font=("Arial Bold", 12))
    set_but.grid(row=3, column=2, rowspan=2, ipady=2, pady=10, sticky=W)

    show_result(good_place[int(combo['values'].index('Novaya Gollandiya'))], txt)

    with open('places.txt', 'w') as f:
        f.write(str(new_places))
