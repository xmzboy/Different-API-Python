import requests
import json
from tkinter import *
from tkinter.ttk import Combobox
from random import uniform
import emoji

places = [('59,9386', '30,3141'), ('61,7632', '31,0061'), ('-45.0311', '168.6626'), ('50.0880', '14.4207'), ('54.7064', '20.5109')]
good_place = []

weather_status = {'Rain': emoji.emojize('rain :cloud_with_rain:'), 'Clear': emoji.emojize('sun :sun:'), 'Clouds': emoji.emojize('clouds :cloud:')}

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
        txt.insert(INSERT, f"Location: {dct['name']}, {dct['sys']['country']}\n"
                           f"Weather: {weather}\n"
                           f"Temperature: {round(dct['main']['temp'] - 273)}\n"
                           f"Feels like: {round(dct['main']['feels_like'] - 273)}\n"
                           f"Humidity: {round(dct['main']['humidity'])}\n"
                           f"Wind speed: {dct['wind']['speed']}\n")
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

window.mainloop()
