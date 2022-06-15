import tkinter
from tkinter import messagebox
from tkinter import ttk
import requests
import pandas
import json

THEME_COLOR = "#1135a7"
LIGHT_BLUE_COLOR = "#1135bf"
LIGHTER_BLUE_COLOR = "#1135de"

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
    window.config(padx=0, pady=0)
    window.geometry("620x750")
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
    global next_button, prev_button, astroFrame, detailsFrame, hourlyFrame, introFrame
    global i
    global hour_data
    global main_frame
    try:
        zip_code_entry1.destroy()
        zip_code_label1.destroy()
        zip_code_entry2.destroy()
        zip_code_label2.destroy()
        zip_code_entry3.destroy()
        zip_code_label3.destroy()
        zip_code_button.destroy()
        title.destroy()
    except NameError:
        pass
    try:
        for widgets in introFrame.winfo_children():
            widgets.destroy()
        for widgets in astroFrame.winfo_children():
            widgets.destroy()
        for widgets in detailsFrame.winfo_children():
            widgets.destroy()
        for widgets in hourlyFrame.winfo_children():
            widgets.destroy()
        astroFrame.destroy()
        detailsFrame.destroy()
        hourlyFrame.destroy()
        introFrame.destroy()
        main_frame.destroy()
    except NameError:
        pass
    second_frame = framing()
    introFrame = tkinter.LabelFrame(second_frame, bg=THEME_COLOR, width=600, highlightthickness=0, bd=0)
    astroFrame = tkinter.LabelFrame(second_frame, text="Astrology", width=600, height=200, labelanchor="n", font=('"Century Schoolbook" 14 bold'), foreground="white", bg=LIGHT_BLUE_COLOR, highlightthickness=0, bd=5)
    detailsFrame = tkinter.LabelFrame(second_frame, text="Details", width=600, height=200, labelanchor="n", font=('"Century Schoolbook" 14 bold'), foreground="white", bg=LIGHT_BLUE_COLOR, highlightthickness=0, bd=5)
    hourlyFrame = tkinter.LabelFrame(second_frame, text="Hourly Forecast", width=600, height=200, labelanchor="n", font=('"Century Schoolbook" 14 bold'), foreground="white", bg=LIGHT_BLUE_COLOR, highlightthickness=0, bd=5)

    date_label = tkinter.Label(introFrame, text=date[i], font=("Century Schoolbook", 25), fg="white", width=17, anchor="w",
                               bg=THEME_COLOR)
    address_label = tkinter.Label(introFrame, text=address, font=("Century Schoolbook", 23), fg="white", width=19, anchor="w",
                                  bg=THEME_COLOR, justify=tkinter.LEFT)
    icon_label = tkinter.Label(introFrame, image=condition_icon[i], text=condition_text[i], compound=tkinter.LEFT, width=360,
                               font=("Century Schoolbook", 23), anchor="w", fg="white", bg=THEME_COLOR)
    temp_label = tkinter.Label(introFrame, text=f"↑ {max_temp[i]}°C\t\t↓ {min_temp[i]}°C", fg="white",
                               font=("Century Schoolbook", 10), width=46, anchor="w", bg=THEME_COLOR)
    ch_prec_label = tkinter.Label(introFrame, text=f"☔ {chance_of_prec[i]}%", font=("Century Schoolbook", 12), bg=THEME_COLOR,
                                  fg="white", pady=1)
    ch_snow_label = tkinter.Label(introFrame, text=f"❄ {chance_of_snow[i]}%", font=("Century Schoolbook", 12), bg=THEME_COLOR,
                                  fg="white", pady=1)
    sunrise_label = tkinter.Label(astroFrame, text=f"Time Of Sunrise: {sunrise[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                                  font=("Century Schoolbook", 10), width=46, anchor="w")
    sunset_label = tkinter.Label(astroFrame, text=f"Time Of Sunset: {sunset[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                                 font=("Century Schoolbook", 10), width=46, anchor="w")
    moonrise_label = tkinter.Label(astroFrame, text=f"Time Of Moonrise: {moonrise[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                                   font=("Century Schoolbook", 10), width=21, anchor="w")
    moonset_label = tkinter.Label(astroFrame, text=f"Time Of Moonset: {moonset[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                                  font=("Century Schoolbook", 10), width=21, anchor="w")
    moonphase_label = tkinter.Label(astroFrame, text=f"Moon Phase: {moon_phase[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                                    font=("Century Schoolbook", 10), width=46, anchor="w")
    prec_label = tkinter.Label(detailsFrame, text=f"Precipitation: {total_prec[i]} mm", bg=LIGHT_BLUE_COLOR, fg="white",
                               font=("Century Schoolbook", 10), width=46, anchor="w")
    hum_label = tkinter.Label(detailsFrame, text=f"Humidity: {avg_humidity[i]}", bg=LIGHT_BLUE_COLOR, fg="white",
                              font=("Century Schoolbook", 10), width=46, anchor="w")
    wind_speed_label = tkinter.Label(detailsFrame, text=f"Wind Speed: {wind_speed[i]} km/h", bg=LIGHT_BLUE_COLOR, fg="white",
                                     font=("Century Schoolbook", 10), width=21, anchor="w")
    vis_label = tkinter.Label(detailsFrame, text=f"Visibility: {avg_visibility[i]} kms.", bg=LIGHT_BLUE_COLOR, fg="white",
                              font=("Century Schoolbook", 10), width=21, anchor="w")

    next_button = tkinter.Button(second_frame, text="Next", fg="white", bg=THEME_COLOR, command=next_button_com)
    prev_button = tkinter.Button(second_frame, text="Previous", fg="white", bg=THEME_COLOR, command=prev_button_com)

    date_label.grid(row=0, column=0, pady=(5, 0), padx=(1, 10), columnspan=3)
    address_label.grid(row=1, column=0, pady=(0, 40), padx=(1, 10), columnspan=3)
    icon_label.grid(row=2, column=0, pady=(40, 0), padx=(1, 10), rowspan=2, columnspan=3)
    temp_label.grid(row=4, column=0, pady=(0, 40), padx=(1, 1), columnspan=3)
    ch_prec_label.grid(row=2, column=3, pady=(40, 0), padx=(10, 0))
    ch_snow_label.grid(row=3, column=3, pady=(0, 0), padx=(10, 0))

    sunrise_label.grid(row=0, column=0, pady=(20, 1), padx=(1, 10))
    sunset_label.grid(row=1, column=0, pady=(1, 1), padx=(1, 10))
    moonrise_label.grid(row=0, column=2, pady=(20, 1), padx=(1, 10))
    moonset_label.grid(row=1, column=2, pady=(1, 1), padx=(1, 10))
    moonphase_label.grid(row=2, column=0, pady=(1, 20), padx=(1, 10), columnspan=2)

    prec_label.grid(row=0, column=0, pady=(20, 1), padx=(1, 10))
    hum_label.grid(row=1, column=0, pady=(1, 20), padx=(1, 10))
    wind_speed_label.grid(row=0, column=1, pady=(20, 1), padx=(1, 10))
    vis_label.grid(row=1, column=1, pady=(1, 20), padx=(1, 10))

    for j in range(0, 24):
        row_num = (j * 4) + 1
        tempFrame = tkinter.LabelFrame(hourlyFrame, bg=LIGHTER_BLUE_COLOR, highlightthickness=0, bd=0)
        time_label = tkinter.Label(tempFrame, text=f"Time: {hour_data[i][j][0]}", fg="white", font=("Century Schoolbook", 12),
                                   width=37, anchor="w", bg=LIGHTER_BLUE_COLOR)
        con_label = tkinter.Label(tempFrame, image=hour_data[i][j][1], text=f"{hour_data[i][j][2]}", compound=tkinter.LEFT,
                                  width=360, font=("Century Schoolbook", 14), anchor="w", fg="white",
                                  bg=LIGHTER_BLUE_COLOR)
        temp_hour_label = tkinter.Label(tempFrame, text=f"{hour_data[i][j][3]}°C", compound=tkinter.LEFT, width=8,
                                        font=("Century Schoolbook", 25), anchor="w", fg="white", bg=LIGHTER_BLUE_COLOR)
        feel_temp_label = tkinter.Label(tempFrame, text=f"Feels like: {hour_data[i][j][4]}°C", bg=LIGHTER_BLUE_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        prec_hour_label = tkinter.Label(tempFrame, text=f"☔ {hour_data[i][j][5]}%", bg=LIGHTER_BLUE_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        snow_hour_label = tkinter.Label(tempFrame, text=f"❄ {hour_data[i][j][6]}%", bg=LIGHTER_BLUE_COLOR, fg="white",
                                        font=("Century Schoolbook", 10), width=21, anchor="w")
        if j == 0:
            time_label.grid(row=0, column=0, pady=(40, 1), padx=(1, 1), columnspan=2)
        else:
            time_label.grid(row=0, column=0, pady=(0, 1), padx=(1, 1), columnspan=2)
        con_label.grid(row=1, column=0, pady=(1, 1), padx=(1, 10), rowspan=2, columnspan=2)
        temp_hour_label.grid(row=1, column=2, pady=(1, 1), padx=(1, 10), rowspan=2)
        feel_temp_label.grid(row=3, column=0, pady=(1, 40), padx=(1, 10))
        prec_hour_label.grid(row=3, column=1, pady=(1, 40), padx=(1, 10))
        snow_hour_label.grid(row=3, column=2, pady=(1, 40), padx=(1, 10))

        tempFrame.grid(row=j, column=0, pady=(20, 20), padx=(5, 5), columnspan=3)

    introFrame.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)
    astroFrame.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)
    detailsFrame.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)
    hourlyFrame.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)
    prev_button.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)
    next_button.pack(padx=10, pady=20, expand=True, fill=tkinter.BOTH)


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
    arrange_forecast_data(data)
    return


def get_my_coordinates():
    geo_address_city = zip_code_entry1.get()
    geo_address_state = zip_code_entry2.get()
    geo_address_country = zip_code_entry3.get()
    global params
    params["key"] = GEOLOC_API_KEY
    params["location"] = f"{geo_address_city}, {geo_address_state}, {geo_address_country}"
    response = requests.get(url=GEOLOC_API, params=params)
    response.raise_for_status()
    data = response.json()
    data = data["results"]
    global my_lat
    global my_lng
    my_lat = data[0]["locations"][0]["displayLatLng"]["lat"]
    my_lng = data[0]["locations"][0]["displayLatLng"]["lng"]
    get_forecast()
    return


zip_code_label1 = tkinter.Label(text="City:", bg=THEME_COLOR, fg="white")
zip_code_entry1 = tkinter.Entry(width=20)
zip_code_label2 = tkinter.Label(text="State:", bg=THEME_COLOR, fg="white")
zip_code_entry2 = tkinter.Entry(width=20)
zip_code_label3 = tkinter.Label(text="Country:", bg=THEME_COLOR, fg="white")
zip_code_entry3 = tkinter.Entry(width=20)
zip_code_button = tkinter.Button(text="Give Me Today's Forecast", bg=THEME_COLOR, fg="white", relief="ridge",
                                 command=get_my_coordinates)

zip_code_entry1.focus()

zip_code_label1.grid(row=1, column=0, pady=(1, 10))
zip_code_entry1.grid(row=1, column=1, pady=(1, 10))
zip_code_label2.grid(row=2, column=0, pady=(1, 10))
zip_code_entry2.grid(row=2, column=1, pady=(1, 10))
zip_code_label3.grid(row=3, column=0, pady=(1, 10))
zip_code_entry3.grid(row=3, column=1, pady=(1, 10))
zip_code_button.grid(row=4, column=0, columnspan=2, pady=(1, 10))
window.mainloop()
