import requests
import json
from tkinter import *
from tkinter.ttk import Combobox
from random import uniform
import emoji
import time
start = time.time()
places = [('59,94', '30,314'), ('61,763', '31,006'), ('-45.031', '168.6626'), ('50.09', '14.42'), ('54.7064', '20.511')]
good_place = []

weather_status = {'Rain': emoji.emojize('rain :umbrella_with_rain_drops:'), 'Clear': emoji.emojize('sun :sun:'),
                  'Clouds': emoji.emojize('clouds :cloud:'), 'Snow': emoji.emojize('snow :snowflake:'),
                  'Fog': emoji.emojize('fog :fog:')}

for i in range(5):
    places.append((uniform(-90, 90), uniform(-180, 180)))

def connection(places, place):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={places[place][0]}&lon={places[place][1]}&appid=8537d9ef6386cb97156fd47d832f479c'
    r = requests.get(url)
    dct = json.loads(r.text)
    return dct

places_name = []
for place in range(len(places)):
    first = connection(places, place)
    if 'country' in first['sys']:
        places_name.append(first['name'])
        good_place.append(places[place])

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
                           f"{emoji.emojize(':globe_with_meridians:')}Coordinates: {dct['coord']['lat']}, {dct['coord']['lon']}")
    except:
        txt.delete(1.0, END)
        txt.insert(INSERT, f"Information is absent")

def callbackFunc(event):
    dct = connection(good_place, int(combo['values'].index(combo.get())))
    show_result(dct)

def set_coord():
    good_place.append((str(lats_entry.get()), str(lons_entry.get())))
    dct = connection(good_place, -1)
    show_result(dct)


window = Tk()
window.title("Weather Here")
window.geometry('400x400')

lbl = Label(window, text="Weather where you are interested?", font=("Arial Bold", 16), justify=CENTER)
lbl.pack()

combo = Combobox(window)
combo['values'] = (places_name)
combo.current(0)
combo.pack()
combo.bind("<<ComboboxSelected>>", callbackFunc)

label = Label(text="Or set your own coordinates:")
label.pack()

lats_entry = Entry()
lats_entry.pack()
lats_entry.insert(0, '50')

lons_entry = Entry()
lons_entry.pack()
lons_entry.insert(0, '0')

set_but = Button(text="Submit", command=set_coord)
set_but.pack()

txt = Text(window, width=30, height=10, font=("Arial Bold", 16))
txt.pack(side=LEFT, expand=True)

dct = connection(good_place, int(combo['values'].index('Novaya Gollandiya')))
show_result(dct)

print(time.time() - start)
window.mainloop()
