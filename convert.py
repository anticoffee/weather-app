from datetime import datetime
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as CTk

# convert temp betweem °C & °F
def convert_temp():
    global default
    global metrics
    global temp_scale

    if default:
        metrics = 'imperial'
        temp_scale = '°F'
        converter_btn.configure(text='Convert to °C')
        default = False
    else:
        metrics = 'metric'
        temp_scale = '°C'
        converter_btn.configure(text='Convert to °F')
        default = True
    return metrics

# finds the weather info of the location input
# find_weather() is instantly run if the user presses the 'enter' key
def find_weather(canvas):

    convert_temp()

    location = user_input.get()

    # uses location, type of metric, and api_key to get the data needed
    api_key = 'd3bf16237ddb9fe0105eb06d591846d8'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units={metrics}&appid={api_key}'
    results = requests.get(url)

    # if the location input is not found, a message box pops up 
    if results.status_code == 404:
       messagebox.showerror(message='City cannot be found')
       return None
    else:
        icon = results.json()['weather'][0]['icon']
        city = results.json()['name']
        country = results.json()['sys']['country']
        description = results.json()['weather'][0]['description']
        temp = round(results.json()['main']['temp'])
        low = round(results.json()['main']['temp_min'])
        high = round(results.json()['main']['temp_max'])
        date = datetime.utcfromtimestamp(results.json()['dt'] + results.json()['timezone'])

        icon_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'

    location_text.configure(text = f'{city}, {country}')

    date_text.configure(text=f'{date}')

    # gets and resize image from url
    icon = Image.open(requests.get(icon_url, stream=True).raw)
    resized_img= icon.resize((140,145))
    img = ImageTk.PhotoImage(resized_img)
  
    img_descr.configure(image=img)
    img_descr.image = img

    temp_text.configure(text=f'{temp}{temp_scale}')

    desc_text.configure(text=f'{description[0].upper()}{description[1:]}')

    minNmax_text.configure(text=f'Highest: {high}{temp_scale}      Lowest: {low}{temp_scale}')

    # prints out the converting button on screen once a location is inputted
    converter_btn.pack(side='bottom', pady=55)

# if user clicks the search_btn, it goes through search () -> find_weather()
def search():
    location = user_input.get()
    data = find_weather(location)

    if data is None:
        return

default = True # used for converting temp button

# prints out the tkinter box on screen
canvas = tk.Tk()
canvas.geometry("500x700")
canvas.title("Weather App")
canvas.configure(bg="#24293E")

# different types of text used
header = ("poppins", 40)
text = ("poppins", 35)
text2 = ("poppins", 25)
micro_text = ("poppins", 20)

# asks for location input
user_input = CTk.CTkEntry(canvas, 
                          font=text2, 
                          text_color="white",
                          fg_color="#2F3651",
                          width=300,
                          height=40,
                          border_width=1)
user_input.pack(pady=(30,15))
user_input.bind('<Return>', find_weather)

search_btn = CTk.CTkButton(canvas, 
                    text='search',
                    command=search,
                    text_color='#24293E',
                    font=("poppins", 18),
                    fg_color="#8EBBFF",
                    hover_color="#DE6F41",
                    height=40,
                    width=100)
search_btn.pack()

# prints all data on screen
location_text = tk.Label(canvas, font=header, bg="#24293E")
location_text.pack(pady=(35,0))

date_text = tk.Label(canvas, font=micro_text, bg="#24293E")
date_text.pack()

img_descr = tk.Label(canvas, bg="#24293E")
img_descr.pack(pady=5)

temp_text = tk.Label(canvas, font=text, bg="#24293E")
temp_text.pack()

desc_text = tk.Label(canvas, font=text, bg="#24293E")
desc_text.pack()

minNmax_text = tk.Label(canvas, font=text2, bg="#24293E")
minNmax_text.pack(pady=(15,0))

converter_btn = CTk.CTkButton(canvas, 
                    command=search,
                    text_color='#24293E',
                    font=("poppins", 18),
                    fg_color="#8EBBFF",
                    hover_color="#DE6F41",
                    height=40,
                    width=160)

canvas.mainloop()