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
            weather = weather_status[dct['weather'][0]['main']]
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


start = time.time()

with open('places.txt') as f:
    places = eval(f.read())
    new_places = []
    new_places.extend(places)

#places = [('59,94', '30,314'), ('61,763', '31,006'), ('-45.031', '168.6626'), ('50.09', '14.42'), ('54.7064', '20.511')]

weather_status = {'Rain': emoji.emojize('rain :umbrella_with_rain_drops:'), 'Clear': emoji.emojize('sun :sun:'),
                  'Clouds': emoji.emojize('clouds :cloud:'), 'Snow': emoji.emojize('snow :snowflake:'),
                  'Fog': emoji.emojize('fog :fog:')}

add_random_places(1, places)
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
window.geometry('400x450')
window.resizable(width=False, height=False)

lbl = Label(window, text=emoji.emojize('Weather Here?:umbrella:'), font=("Arial Bold", 16), justify=CENTER)
lbl.grid(row=0, column=1, sticky=W)

label = Label(text="Choose a place:", font=("Arial Bold", 12))
label.grid(row=1, column=0, sticky=E)

combo = Combobox(window)
combo['values'] = (places_name)
combo.current(0)
combo.grid(row=1, column=1, columnspan=2, sticky=W, ipadx=20)
combo.bind("<<ComboboxSelected>>", callbackFunc)

label = Label(text="Or set your own coordinates:", font=("Arial Bold", 12))
label.grid(row=2, column=0, columnspan=3)

lats_label = Label(text="Latitude:", font=("Arial Bold", 12))
lats_label.grid(row=3, column=0, sticky=E)

lats_entry = Entry()
lats_entry.grid(row=3, column=1, sticky=W)
lats_entry.insert(0, '50')

lons_label = Label(text="Longitude:", font=("Arial Bold", 12))
lons_label.grid(row=4, column=0, sticky=E)

lons_entry = Entry()
lons_entry.grid(row=4, column=1, sticky=W)
lons_entry.insert(0, '0')

set_but = Button(text="Submit", command=set_coord, font=("Arial Bold", 14))
set_but.grid(row=3, column=1, rowspan=2, sticky=E)

add_new_button = Button(text="Add new place", command=record_new_place, font=("Arial Bold", 12))
add_new_button.grid(row=5, column=0, ipady=5, pady=10, sticky=E)

delete_button = Button(text="Delete place", command=record_new_place, font=("Arial Bold", 12))
delete_button.grid(row=5, column=1, ipady=5, ipadx=5, pady=10, sticky=E)

txt = Text(window, width=30, height=10, font=("Arial Bold", 16))
txt.grid(row=6, column=0, columnspan=3, padx=10, ipadx=7)
#txt.pack(side=LEFT, expand=True)

show_result(good_place[int(combo['values'].index('Novaya Gollandiya'))])

print(time.time() - start)
window.mainloop()

with open('places.txt', 'w') as f:
    f.write(str(new_places))