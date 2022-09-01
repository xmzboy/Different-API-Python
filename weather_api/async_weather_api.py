import grequests
import requests
import json
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.messagebox as mb
from random import uniform
import emoji
import time

from rec_data import record_data


def log_dec(func):
    def wrap(*args, **kwargs):
        print(f"Start {func.__name__}")
        start_f = time.time()
        result = func(*args, **kwargs)
        print(f"Stop {func.__name__}, executing time = {time.time() - start_f}")
        return result
    return wrap


def connection(places, place):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={places[place][0]}&lon={places[place][1]}&appid=8537d9ef6386cb97156fd47d832f479c'
    return url


@log_dec
def one_connect(lats, lons):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lats}&lon={lons}&appid=8537d9ef6386cb97156fd47d832f479c'
    r = requests.get(url)
    return json.loads(r.text)


def show_result(dct):
    try:
        txt.delete(1.0, END)
        try:
            weather = WEATHER_STATUS[dct['weather'][0]['main']]
        except:
            weather = dct['weather'][0]['main']
        txt.insert(INSERT, f"{emoji.emojize(':globe_showing_Americas:')}Location: {dct['name']}, {dct['sys']['country']}\n"
                           f"{emoji.emojize(':seedling:')}Weather: {weather}\n"
                           f"{emoji.emojize(':fire:')}Temperature: {round(dct['main']['temp'] - 273)}\n"
                           f"{emoji.emojize(':fallen_leaf:')}Feels like: {round(dct['main']['feels_like'] - 273)}\n"
                           f"{emoji.emojize(':droplet:')}Humidity: {round(dct['main']['humidity'])}\n"
                           f"{emoji.emojize(':cyclone:')}Wind speed: {dct['wind']['speed']}\n"
                           f"{emoji.emojize(':globe_with_meridians:')}Coordinates: {round(dct['coord']['lat'], 2)}, {round(dct['coord']['lon'], 2)}")
    except:
        txt.delete(1.0, END)
        txt.insert(INSERT, f"Information is absent")


def record_new_place():
    new_places.append((str(lats_entry.get()), str(lons_entry.get())))
    mb.showinfo("Information", "Your data has been successfully saved")


def get_manual():
    mb.showinfo("Manual", "Welcome to the Weather API Application Manual!\n"
                          "This application will show you the weather in selected cities or at given coordinates.\n"
                          "To search for information about the weather in one of the cities, select this city in the"
                          "drop-down list. The data itself will appear in the text box below.\n"
                          "To search for weather information by coordinates, enter the latitude of the place you are"
                          "looking for in the 'Latitude' field, and its longitude in the 'Longitude' field. Click on"
                          "the 'Search' button and enjoy the result given in the text field.\n"
                          "To save a place in the drop-down list, enter the coordinates, click on the settings button,"
                          " and then on the 'Add place' button. If the location has been successfully added, a"
                          " notification will appear. Restart the program and enjoy the result.\n"
                          "To remove a place from the list, select the place from the list above the 'Delete' \n"
                          "and press the 'Delete' button. If the deletion was successful, a notification will appear.\n"
                          "Restart the program and enjoy the result.")


def callbackFunc(event):
    show_result(good_place[int(combo['values'].index(combo.get()))])


@log_dec
def set_coord():
    dct = one_connect(str(lats_entry.get()), str(lons_entry.get()))
    show_result(dct)


@log_dec
def get_responses_lst(places):
    places_urls = []
    for place in range(len(places)):
        places_urls.append(connection(places, place))

    async_list = []
    for u in places_urls:
        start_loop = time.time()
        print("Start loop")
        action_item = grequests.get(u)
        async_list.append(action_item)
        print("Url =", u)
        print(f"End loop, time = {time.time() - start_loop}")
    return grequests.map(async_list)


@log_dec
def add_random_places(count, places):
    for i in range(count):
        places.append((uniform(-90, 90), uniform(-180, 180)))


def recording_data(lst):
    record_data(lst[2])
    record_data(lst[5])


def delete_place():
    pass


def settings():
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry('230x230')
    settings_window.resizable(width=False, height=False)

    lbl = Label(settings_window, text='     ', font=("Arial Bold", 20))
    lbl.grid(row=0, column=0)

    manual_button = Button(settings_window, text="     Manual    ", command=get_manual, font=("Arial Bold", 14))
    manual_button.grid(row=0, column=1, sticky=W+E, pady=10)

    add_new_button = Button(settings_window, text="  Add place  ", command=record_new_place, font=("Arial Bold", 14))
    add_new_button.grid(row=2, column=1, sticky=W+E, pady=10)

    emp_lbl = Label(settings_window, text='     ', font=("Arial Bold", 14))
    emp_lbl.grid(row=4, column=1)

    delete_combo = Combobox(settings_window)
    delete_combo['values'] = (places_name)
    delete_combo.current(0)
    delete_combo.grid(row=5, column=1)
    delete_combo.bind("<<ComboboxSelected>>", callbackFunc)

    delete_button = Button(settings_window, text="Delete place", command=delete_place, font=("Arial Bold", 14))
    delete_button.grid(row=6, column=1, sticky=W+E, pady=10)


start = time.time()

with open('places.txt') as f:
    places = eval(f.read())
    new_places = []
    new_places.extend(places)

WEATHER_STATUS = {'Rain': emoji.emojize('rain :umbrella_with_rain_drops:'),
                  'Clear': emoji.emojize('sun :sun:'),
                  'Clouds': emoji.emojize('clouds :cloud:'),
                  'Snow': emoji.emojize('snow :snowflake:'),
                  'Fog': emoji.emojize('fog :fog:')}

# add_random_places(1, places)
responses_lst = get_responses_lst(places)

lst, places_name, good_place = [], [], []
for resp in responses_lst:
    lst.append(json.loads(resp.text))

for dct in lst:
    if 'country' in dct['sys']:
        if dct['name'] not in places_name:
            places_name.append(dct['name'])
            good_place.append(dct)

recording_data(lst)

window = Tk()
window.title("Weather Here")
window.geometry('400x400')
window.resizable(width=False, height=False)

lbl = Label(window, text='', font=("Arial Bold", 2))
lbl.grid(row=0, column=1)

label = Label(text="Choose a place:", font=("Arial Bold", 12))
label.grid(row=1, column=0, sticky=E)

combo = Combobox(window)
combo['values'] = (places_name)
combo.current(0)
combo.grid(row=1, column=1, sticky=W, ipadx=15)
combo.bind("<<ComboboxSelected>>", callbackFunc)

settings_button = Button(text=emoji.emojize(':gear:'), command=settings, font=("Arial Bold", 14))
settings_button.grid(row=1, column=2, ipady=2, sticky=W, ipadx=1)

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

set_but = Button(text="Search", command=set_coord, font=("Arial Bold", 12))
set_but.grid(row=3, column=2, rowspan=2, ipady=2, pady=10, sticky=W)

txt = Text(window, width=27, height=10, font=("Arial Bold", 16))
txt.grid(row=6, column=0, columnspan=3, padx=20, ipadx=15, sticky=W+E)

show_result(good_place[int(combo['values'].index('Novaya Gollandiya'))])

print(time.time() - start)
window.mainloop()

with open('places.txt', 'w') as f:
    f.write(str(new_places))