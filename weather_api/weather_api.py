import requests
from tkinter import *
from tkinter.ttk import Combobox
from random import uniform
import emoji


places = [('59,94', '30,314'), ('61,763', '31,006'), ('-45.031', '168.6626'), ('50.09', '14.42'), ('54.7064', '20.511')]
good_place, places_name = [], []
weather_status = {'Rain': emoji.emojize('rain :umbrella_with_rain_drops:'), 'Clear': emoji.emojize('sun :sun:'),
                  'Clouds': emoji.emojize('clouds :cloud:'), 'Snow': emoji.emojize('snow :snowflake:'),
                  'Fog': emoji.emojize('fog :fog:')}

for i in range(5):
    places.append((uniform(-90, 90), uniform(-180, 180)))


def connection(con_places, con_place):
    """Get data from weather api"""
    params = {
        'lat': con_places[con_place][0],
        'lon': con_places[con_place][1],
        'appid': '8537d9ef6386cb97156fd47d832f479c'
        }
    url = 'https://api.openweathermap.org/data/2.5/weather'
    r = requests.get(url, params=params)
    return r.json()


for place in range(len(places)):
    first = connection(places, place)
    if 'country' in first['sys']:
        places_name.append(first['name'])
        good_place.append(places[place])


def show_result(show_dct):
    """Show weather information in text block"""
    try:
        txt.delete(1.0, END)
        try:
            weather = weather_status[show_dct['weather'][0]['main']]
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
        txt.insert(INSERT, f"Information is absent")


def list_callback(event):
    """List callback"""
    show_result(connection(good_place, int(combo['values'].index(combo.get()))))


def set_coord():
    """Setting place coordinates"""
    good_place.append((str(lats_entry.get()), str(lons_entry.get())))
    show_result(connection(good_place, -1))


window = Tk()
window.title("Weather Here")
window.geometry('400x400')

lbl = Label(window, text="Weather where you are interested?", font=("Arial Bold", 16), justify=CENTER)
lbl.pack()

combo = Combobox(window)
combo['values'] = places_name
combo.current(0)
combo.pack()
combo.bind("<<ComboboxSelected>>", list_callback)

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

dct = connection(good_place, 0)
show_result(dct)
window.mainloop()
