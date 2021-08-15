import tkinter
from tkinter import messagebox
from tkinter import ttk
import requests
import pandas
import json

THEME_COLOR = "#1135a7"
data_file = pandas.read_csv("data.csv")
data_file_name = list(data_file["name"])
data_file_data = list(data_file["data"])
WEATHER_API_KEY = data_file_data[data_file_name.index("WEATHER_API_KEY")]
WEATHER_API = data_file_data[data_file_name.index("WEATHER_API")]
GEOLOC_API_KEY = data_file_data[data_file_name.index("GEOLOC_API_KEY")]
GEOLOC_API = data_file_data[data_file_name.index("GEOLOC_API")]
global params
global my_lat
global my_lng
params = {}

window = tkinter.Tk()
window.title("Weather Forecast")
window.config(padx=20, pady=20, bg=THEME_COLOR, height=200)

title = tkinter.Label(text="Weather Forecast", bg=THEME_COLOR, fg="white", font=("Century Schoolbook", 24))
title.grid(row=0, column=0, columnspan=2, pady=(1, 10))

global date, address, max_temp, min_temp, avg_temp, wind_speed, total_prec, avg_humidity, chance_of_prec, chance_of_snow, condition_text, condition_icon, sunrise, sunset, moonrise, moonset, moon_phase, uv, avg_visibility
address = ""
date = []
max_temp = []
min_temp = []
avg_temp = []
wind_speed = []
total_prec = []
avg_humidity = []
chance_of_prec = []
chance_of_snow = []
condition_text = []
condition_icon = []
sunrise = []
sunset = []
moonrise = []
moonset = []
moon_phase = []
uv = []
avg_visibility = []

global i
i = 0


def framing():
    global main_frame
    window.config(padx =0, pady=0)
    main_frame = tkinter.Frame(window)
    main_frame.pack(fill=tkinter.BOTH, expand=1)

    my_canvas = tkinter.Canvas(main_frame, bg=THEME_COLOR, width=550, height=700)
    my_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=tkinter.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = tkinter.Frame(my_canvas, bg=THEME_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    return second_frame


def next_button_com():
    global i, next_button, prev_button
    prev_button.config(state="active")
    if i == 2:
        next_button.config(state="disabled")
        display_data()
        return
    i = (i + 1)
    display_data()
    return


def prev_button_com():
    global i, next_button, prev_button
    next_button.config(state="active")
    if i in (1, 2):
        i = (i - 1)
    if i == 0:
        prev_button.config(state="disabled")
    display_data()
    return


def display_data():
    global date, address, max_temp, min_temp, avg_temp, wind_speed, total_prec, avg_humidity, chance_of_prec, chance_of_snow, condition_text, condition_icon, sunrise, sunset, moonrise, moonset, moon_phase, uv, avg_visibility
    global date_label, address_label, icon_label, temp_label, ch_prec_label, ch_snow_label, details_1_label, sunrise_label, sunset_label, moonrise_label, moonset_label, moonphase_label, details_2_label, prec_label, hum_label, wind_speed_label, vis_label, next_button, prev_button
    global i
    global hour_data
    global main_frame
    try:
        zip_code_entry1.destroy()
        zip_code_label1.destroy()
        zip_code_entry2.destroy()
        zip_code_label2.destroy()
        zip_code_button.destroy()
        title.destroy()
    except NameError:
        pass
    try:
        date_label.destroy()
        address_label.destroy()
        icon_label.destroy()
        temp_label.destroy()
        ch_snow_label.destroy()
        ch_prec_label.destroy()
        details_1_label.destroy()
        sunrise_label.destroy()
        sunset_label.destroy()
        moonrise_label.destroy()
        moonset_label.destroy()
        moonphase_label.destroy()
        details_2_label.destroy()
        prec_label.destroy()
        hum_label.destroy()
        wind_speed_label.destroy()
        vis_label.destroy()
        main_frame.destroy()
    except NameError:
        pass
    second_frame = framing()
    date_label = tkinter.Label(second_frame, text=date[i], font=("Century Schoolbook", 25), fg="white", width=17, anchor="w",
                               bg=THEME_COLOR)
    address_label = tkinter.Label(second_frame, text=address, font=("Century Schoolbook", 23), fg="white", width=19, anchor="w",
                                  bg=THEME_COLOR, justify=tkinter.LEFT)
    icon_label = tkinter.Label(second_frame, image=condition_icon[i], text=condition_text[i], compound=tkinter.LEFT, width=360,
                               font=("Century Schoolbook", 23), anchor="w", fg="white", bg=THEME_COLOR)
    temp_label = tkinter.Label(second_frame, text=f"↑ {max_temp[i]}°C\t\t↓ {min_temp[i]}°C", fg="white",
                               font=("Century Schoolbook", 10), width=46, anchor="w", bg=THEME_COLOR)
    ch_prec_label = tkinter.Label(second_frame, text=f"☔ {chance_of_prec[i]}%", font=("Century Schoolbook", 12), bg=THEME_COLOR,
                                  fg="white", pady=1)
    ch_snow_label = tkinter.Label(second_frame, text=f"❄ {chance_of_snow[i]}%", font=("Century Schoolbook", 12), bg=THEME_COLOR,
                                  fg="white", pady=1)
    details_1_label = tkinter.Label(second_frame, text="Astrology", fg="white", font=("Century Schoolbook", 16), width=29, anchor="w",
                                    bg=THEME_COLOR)
    sunrise_label = tkinter.Label(second_frame, text=f"Time Of Sunrise: {sunrise[i]}", bg=THEME_COLOR, fg="white",
                                  font=("Century Schoolbook", 10), width=22, anchor="w")
    sunset_label = tkinter.Label(second_frame, text=f"Time Of Sunset: {sunset[i]}", bg=THEME_COLOR, fg="white",
                                 font=("Century Schoolbook", 10), width=22, anchor="w")
    moonrise_label = tkinter.Label(second_frame, text=f"Time Of Moonrise: {moonrise[i]}", bg=THEME_COLOR, fg="white",
                                   font=("Century Schoolbook", 10), width=21, anchor="w")
    moonset_label = tkinter.Label(second_frame, text=f"Time Of Moonset: {moonset[i]}", bg=THEME_COLOR, fg="white",
                                  font=("Century Schoolbook", 10), width=21, anchor="w")
    moonphase_label = tkinter.Label(second_frame, text=f"Moon Phase: {moon_phase[i]}", bg=THEME_COLOR, fg="white",
                                    font=("Century Schoolbook", 10), width=46, anchor="w")
    details_2_label = tkinter.Label(second_frame, text="Details", fg="white", font=("Century Schoolbook", 16), width=29, anchor="w",
                                    bg=THEME_COLOR)
    prec_label = tkinter.Label(second_frame, text=f"Precipitation: {total_prec[i]} mm", bg=THEME_COLOR, fg="white",
                               font=("Century Schoolbook", 10), width=22, anchor="w")
    hum_label = tkinter.Label(second_frame, text=f"Humidity: {avg_humidity[i]}", bg=THEME_COLOR, fg="white",
                              font=("Century Schoolbook", 10), width=22, anchor="w")
    wind_speed_label = tkinter.Label(second_frame, text=f"Wind Speed: {wind_speed[i]} km/h", bg=THEME_COLOR, fg="white",
                                     font=("Century Schoolbook", 10), width=21, anchor="w")
    vis_label = tkinter.Label(second_frame, text=f"Visibility: {avg_visibility[i]} kms.", bg=THEME_COLOR, fg="white",
                              font=("Century Schoolbook", 10), width=21, anchor="w")
    details_3_label = tkinter.Label(second_frame, text="Hourly Forecast", fg="white", font=("Century Schoolbook", 16), width=29, anchor="w",
                                    bg=THEME_COLOR)
    next_button = tkinter.Button(second_frame, text="Next", fg="white", bg=THEME_COLOR, command=next_button_com)
    prev_button = tkinter.Button(second_frame, text="Previous", fg="white", bg=THEME_COLOR, command=prev_button_com)


    date_label.grid(row=0, column=0, pady=(5, 0), padx=(1, 10), columnspan=2)
    address_label.grid(row=1, column=0, pady=(0, 40), padx=(1, 10), columnspan=2)
    icon_label.grid(row=2, column=0, pady=(40, 0), padx=(1, 10), rowspan=2, columnspan=2)
    temp_label.grid(row=4, column=0, pady=(0, 40), padx=(1, 1), columnspan=2)
    ch_prec_label.grid(row=2, column=2, pady=(40, 0), padx=(10, 0))
    ch_snow_label.grid(row=3, column=2, pady=(0, 0), padx=(10, 0))
    details_1_label.grid(row=5, column=0, pady=(40, 1), padx=(1, 1), columnspan=2)
    sunrise_label.grid(row=6, column=0, pady=(1, 1), padx=(1, 10))
    sunset_label.grid(row=7, column=0, pady=(1, 1), padx=(1, 10))
    moonrise_label.grid(row=6, column=1, pady=(1, 1), padx=(1, 10))
    moonset_label.grid(row=7, column=1, pady=(1, 1), padx=(1, 10))
    moonphase_label.grid(row=8, column=0, pady=(1, 40), padx=(1, 10), columnspan=2)
    details_2_label.grid(row=9, column=0, pady=(40, 1), padx=(1, 1), columnspan=2)
    prec_label.grid(row=10, column=0, pady=(1, 1), padx=(1, 10))
    hum_label.grid(row=11, column=0, pady=(1, 40), padx=(1, 10))
    wind_speed_label.grid(row=10, column=1, pady=(1, 1), padx=(1, 10))
    vis_label.grid(row=11, column=1, pady=(1, 40), padx=(1, 10))
    details_3_label.grid(row=12, column=0, pady=(40, 1), padx=(1, 1), columnspan=2)

    x = 12
    for j in range(0, 24):
        row_num = x + (j * 4) + 1
        time_label = tkinter.Label(second_frame, text=f"Time: {hour_data[i][j][0]}", fg="white", font=("Century Schoolbook", 12),
                                   width=37, anchor="w", bg=THEME_COLOR)
        con_label = tkinter.Label(second_frame, image=hour_data[i][j][1], text=f"{hour_data[i][j][2]}", compound=tkinter.LEFT,
                                  width=360, font=("Century Schoolbook", 14), anchor="w", fg="white",
                                  bg=THEME_COLOR)
        temp_hour_label = tkinter.Label(second_frame, text=f"{hour_data[i][j][3]}°C", compound=tkinter.LEFT, width=8,
                                        font=("Century Schoolbook", 25), anchor="w", fg="white", bg=THEME_COLOR)
        feel_temp_label = tkinter.Label(second_frame, text=f"Feels like: {hour_data[i][j][4]}°C", bg=THEME_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        prec_hour_label = tkinter.Label(second_frame, text=f"☔ {hour_data[i][j][5]}%", bg=THEME_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        snow_hour_label = tkinter.Label(second_frame, text=f"❄ {hour_data[i][j][6]}%", bg=THEME_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        time_label.grid(row=row_num, column=0, pady=(0, 1), padx=(1, 1), columnspan=2)
        con_label.grid(row=row_num + 1, column=0, pady=(1, 1), padx=(1, 10), rowspan=2, columnspan=2)
        temp_hour_label.grid(row=row_num + 1, column=2, pady=(1, 1), padx=(1, 10), rowspan=2)
        feel_temp_label.grid(row=row_num + 3, column=0, pady=(1, 40), padx=(1, 10))
        prec_hour_label.grid(row=row_num + 3, column=1, pady=(1, 40), padx=(1, 10))
        snow_hour_label.grid(row=row_num + 3, column=2, pady=(1, 40), padx=(1, 10))

    next_button.grid(row=109, column=1, pady=(20, 1), padx=(1, 1), columnspan=2)
    prev_button.grid(row=109, column=0, pady=(20, 1), padx=(1, 1))


def arrange_data_hourly(data):
    global hour_data
    hour_data = []
    for i in range(0, 3):
        day_data = []
        mod_data = data[i]["hour"]
        for j in range(0, 24):
            one_data = []
            time = mod_data[j]["time"][-5:]
            temp = mod_data[j]["temp_c"]
            con_text = mod_data[j]["condition"]["text"]
            con_icon = mod_data[j]["condition"]["icon"].split("/")
            con_icon = con_icon[-2] + "/" + con_icon[-1]
            icon_loc = f"./icons/{con_icon}"
            photo = tkinter.PhotoImage(file=icon_loc)
            rain = mod_data[j]["chance_of_rain"]
            snow = mod_data[j]["chance_of_snow"]
            feel_temp = mod_data[j]["feelslike_c"]
            one_data.append(time)
            one_data.append(photo)
            one_data.append(con_text)
            one_data.append(temp)
            one_data.append(feel_temp)
            one_data.append(rain)
            one_data.append(snow)
            day_data.append(one_data)
        hour_data.append(day_data)


def arrange_forecast_data(data):
    global date, address, max_temp, min_temp, avg_temp, wind_speed, total_prec, avg_humidity, chance_of_prec, chance_of_snow, condition_text, condition_icon, sunrise, sunset, moonrise, moonset, moon_phase, uv, avg_visibility
    address = f"{data['location']['name']},\n{data['location']['region']},\n{data['location']['country']}"
    data = data["forecast"]["forecastday"]
    for i in range(0, 3):
        date.append(data[i]["date"])
        max_temp.append(data[i]["day"]["maxtemp_c"])
        min_temp.append(data[i]["day"]["mintemp_c"])
        avg_temp.append(data[i]["day"]["avgtemp_c"])
        wind_speed.append(data[i]["day"]["maxwind_kph"])
        total_prec.append(data[i]["day"]["totalprecip_mm"])
        avg_humidity.append(data[i]["day"]["avghumidity"])
        chance_of_prec.append(data[i]["day"]["daily_chance_of_rain"])
        chance_of_snow.append(data[i]["day"]["daily_chance_of_snow"])
        condition_text.append(data[i]["day"]["condition"]["text"])
        condition_icon.append(data[i]["day"]["condition"]["icon"])
        sunrise.append(data[i]["astro"]["sunrise"])
        sunset.append(data[i]["astro"]["sunset"])
        moonrise.append(data[i]["astro"]["moonrise"])
        moonset.append(data[i]["astro"]["moonset"])
        moon_phase.append(data[i]["astro"]["moon_phase"])
        uv.append(data[i]["day"]["uv"])
        avg_visibility.append(data[i]["day"]["avgvis_km"])

    for i in range(0, 3):
        cond_icon = condition_icon[i].split("/")
        cond_icon = cond_icon[-2] + "/" + cond_icon[-1]
        icon_loc = f"./icons/{cond_icon}"
        photo = tkinter.PhotoImage(file=icon_loc)
        condition_icon[i] = photo
    arrange_data_hourly(data)
    display_data()
    return


def get_forecast():
    global my_lat
    global my_lng
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{my_lat},{my_lng}",
        "days": 3,
    }
    response = requests.get(url=WEATHER_API, params=params)
    response.raise_for_status()
    data = response.json()
    with open("weather.json", "w") as file:
        json.dump(data, file, indent=4)
    arrange_forecast_data(data)
    return


def get_my_coordinates():
    geo_address = zip_code_entry1.get()
    zip_code = zip_code_entry2.get()
    if zip_code == "":
        messagebox.showerror(title="Error", message="Please enter zip-code!")
        return
    try:
        int(zip_code)
    except ValueError:
        pass
    global params
    params["key"] = GEOLOC_API_KEY
    params["location"] = f"{geo_address}, {zip_code}"
    response = requests.get(url=GEOLOC_API, params=params)
    response.raise_for_status()
    data = response.json()
    data = data["results"]
    with open("loc.json", "w") as file:
        json.dump(data, file, indent=4)
    global my_lat
    global my_lng
    my_lat = data[0]["locations"][0]["displayLatLng"]["lat"]
    my_lng = data[0]["locations"][0]["displayLatLng"]["lng"]
    with open("loc.json", "w") as file:
        json.dump(data, file, indent=4)
    get_forecast()
    return


zip_code_label1 = tkinter.Label(text="Address:", bg=THEME_COLOR, fg="white")
zip_code_entry1 = tkinter.Entry(width=20)
zip_code_label2 = tkinter.Label(text="Pin-Code/Zip-Code:", bg=THEME_COLOR, fg="white")
zip_code_entry2 = tkinter.Entry(width=20)
zip_code_button = tkinter.Button(text="Give Me Today's Forecast", bg=THEME_COLOR, fg="white", relief="ridge",
                                 command=get_my_coordinates)

zip_code_entry1.focus()

zip_code_label1.grid(row=1, column=0, pady=(1, 10))
zip_code_entry1.grid(row=1, column=1, pady=(1, 10))
zip_code_label2.grid(row=2, column=0, pady=(1, 10))
zip_code_entry2.grid(row=2, column=1, pady=(1, 10))
zip_code_button.grid(row=3, column=0, columnspan=2, pady=(1, 10))
window.mainloop()
