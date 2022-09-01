import csv
import datetime

SEASONS = {(12, 1, 2): 'Winter', (3, 4, 5):'Spring', (6, 7, 8): 'Summer', (9, 10, 11): 'Fall'}


def get_season(dct):
    for k, v in SEASONS.items():
        if datetime.date.today().month in k:
            if dct['coord']['lat'] < 0:
                temp = datetime.date.today().month + 6
                if temp > 12:
                    temp -= 12
                for key in SEASONS.keys():
                    if temp in key:
                        return SEASONS[key]
            else:
                return v


def record_data(dct):
    filename = f"data/{dct['name'].lower().replace(' ', '_')}_data.csv"
    season = get_season(dct)
    lst = [datetime.date.today().strftime('%d %B %Y'), season,
           dct['weather'][0]['main'], round(dct['main']['temp'] - 273),
           round(dct['main']['humidity']), round(dct['wind']['speed'])]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            final_data = f.readlines()[-1]
    except:
        with open(filename, 'w', encoding='utf-8') as f:
            file_writer = csv.writer(f, delimiter=";", lineterminator="\r")
            file_writer.writerow(["Date", "Season", "Weather", "Temperature", "Humidity", "Wind Speed"])
            file_writer.writerow(lst)
    else:
        if final_data.split(';')[0] != lst[0]:
            with open(filename, 'a', encoding='utf-8') as f:
                file_writer = csv.writer(f, delimiter=";", lineterminator="\r")
                file_writer.writerow(lst)
