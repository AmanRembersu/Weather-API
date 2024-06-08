import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk

def get_weather(city):
    API_KEY = "3eeeeb3a06b9b029c12d84d9d047596d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    res = requests.get(url) 

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city_name, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, description, city_name, country = result
    location_label.configure(text=f"{city_name}, {country}")
    
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

root = ttk.Window(themename="morph")
root.title("Weathery")
root.geometry("400x400")

city_entry = ttk.Entry(root, font="Fantasy, 18")
city_entry.pack(pady=10)

search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

location_label = tk.Label(root, font="fantasy 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="fantasy 20")
temperature_label.pack()

description_label = tk.Label(root, font="fantasy 20")
description_label.pack()

root.mainloop()
