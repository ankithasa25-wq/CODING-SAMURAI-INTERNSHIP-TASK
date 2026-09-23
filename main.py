import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- LOAD API KEY ----------------

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


dark_mode = False


# ---------------- THEME ----------------

light_theme = {
    "bg": "#eef2f7",
    "card": "#ffffff",
    "text": "#1f2937",
    "secondary": "#64748b",
    "button": "#e2e8f0"
}

dark_theme = {
    "bg": "#151922",
    "card": "#222936",
    "text": "#f8fafc",
    "secondary": "#cbd5e1",
    "button": "#374151"
}


# ---------------- WEATHER ICON ----------------

def get_weather_icon(condition):

    condition = condition.lower()

    if "thunderstorm" in condition:
        return "⛈️"

    elif "rain" in condition or "drizzle" in condition:
        return "🌧️"

    elif "snow" in condition:
        return "❄️"

    elif "cloud" in condition:
        return "☁️"

    elif "clear" in condition:
        return "☀️"

    elif "mist" in condition or "fog" in condition:
        return "🌫️"

    else:
        return "🌤️"


# ---------------- WEATHER ADVICE ----------------

def get_weather_advice(temperature, condition):

    condition = condition.lower()

    if "thunderstorm" in condition:
        return "⛈️ Thunderstorm conditions are reported. Take care outdoors."

    elif "rain" in condition or "drizzle" in condition:
        return "🌧️ Rain is currently reported. Consider carrying an umbrella."

    elif temperature >= 35:
        return "🥵 It is very hot. Stay hydrated and avoid prolonged heat."

    elif temperature >= 30:
        return "🌡️ It is quite warm. Stay hydrated."

    elif temperature >= 20:
        return "😊 The temperature is comfortable."

    elif temperature >= 15:
        return "🧥 The temperature is slightly cool. A light jacket may help."

    else:
        return "❄️ It is cold. Consider wearing warm clothing."


# ---------------- GET WEATHER ----------------

def get_weather():

    city = city_entry.get().strip()

    if not city:

        messagebox.showwarning(
            "Input Error",
            "Please enter a city name."
        )

        return

    current_url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            current_url,
            params=params,
            timeout=10
        )

        if response.status_code == 404:

            messagebox.showerror(
                "City Not Found",
                "Please check the city name and try again."
            )

            return

        if response.status_code == 401:

            messagebox.showerror(
                "API Error",
                "Invalid API key."
            )

            return

        response.raise_for_status()

        data = response.json()

        city_name = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        wind_speed = data["wind"]["speed"]

        condition = data["weather"][0]["description"]

        icon = get_weather_icon(condition)

        condition_lower = condition.lower()

        if "thunderstorm" in condition_lower:
            category = "Thunderstorm"

        elif "rain" in condition_lower or "drizzle" in condition_lower:
            category = "Rainy"

        elif "cloud" in condition_lower:
            category = "Cloudy"

        elif "clear" in condition_lower:
            category = "Clear"

        elif "snow" in condition_lower:
            category = "Snowy"

        elif "mist" in condition_lower or "fog" in condition_lower:
            category = "Low Visibility"

        else:
            category = "Other"

        advice = get_weather_advice(
            temperature,
            condition
        )

        update_time = datetime.now().strftime(
            "%d-%m-%Y  %I:%M:%S %p"
        )

        result_text.set(
            f"{icon}  {city_name}, {country}\n\n"
            f"🌡 Temperature   : {temperature:.1f} °C\n"
            f"🌡 Feels Like    : {feels_like:.1f} °C\n"
            f"☁ Condition     : {condition.title()}\n"
            f"📊 Category      : {category}\n"
            f"💧 Humidity      : {humidity}%\n"
            f"💨 Wind Speed    : {wind_speed} m/s\n"
            f"🔵 Pressure      : {pressure} hPa\n"
            f"🕒 Updated At    : {update_time}"
        )

        advice_text.set(advice)

        get_forecast(city)

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Connection Error",
            "Please check your internet connection."
        )

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Timeout",
            "The weather service took too long to respond."
        )

    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Error",
            "Unable to retrieve weather data."
        )

    except KeyError:

        messagebox.showerror(
            "Data Error",
            "Unexpected data received from the weather API."
        )


# ---------------- REFRESH ----------------

def refresh_weather():

    city = city_entry.get().strip()

    if not city:

        messagebox.showwarning(
            "Input Error",
            "Please enter a city name first."
        )

        return

    get_weather()


# ---------------- FORECAST ----------------

def get_forecast(city):

    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast"
    )

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            forecast_url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            forecast_text.set(
                "Forecast unavailable."
            )

            return

        data = response.json()

        daily_data = {}

        for item in data["list"]:

            date = item["dt_txt"].split(" ")[0]

            temperature = item["main"]["temp"]

            condition = item["weather"][0]["description"]

            if date not in daily_data:

                daily_data[date] = {
                    "min": temperature,
                    "max": temperature,
                    "condition": condition
                }

            else:

                daily_data[date]["min"] = min(
                    daily_data[date]["min"],
                    temperature
                )

                daily_data[date]["max"] = max(
                    daily_data[date]["max"],
                    temperature
                )

        forecast_output = ""

        dates = []
        min_temperatures = []
        max_temperatures = []

        count = 0

        for date, values in daily_data.items():

            icon = get_weather_icon(
                values["condition"]
            )

            forecast_output += (
                f"{icon}  {date}\n"
                f"    Min Temperature : "
                f"{values['min']:.1f} °C\n"
                f"    Max Temperature : "
                f"{values['max']:.1f} °C\n"
                f"    Condition       : "
                f"{values['condition'].title()}\n\n"
            )

            dates.append(date)

            min_temperatures.append(
                values["min"]
            )

            max_temperatures.append(
                values["max"]
            )

            count += 1

            if count == 5:
                break

        forecast_text.set(
            forecast_output
        )

        create_temperature_chart(
            dates,
            min_temperatures,
            max_temperatures,
            city
        )

    except requests.exceptions.RequestException:

        forecast_text.set(
            "Unable to retrieve forecast."
        )


# ---------------- TEMPERATURE CHART ----------------

def create_temperature_chart(
        dates,
        min_temperatures,
        max_temperatures,
        city
):

    for widget in chart_frame.winfo_children():
        widget.destroy()

    if not dates:
        return

    figure = plt.Figure(
        figsize=(7, 3.5),
        dpi=100
    )

    axis = figure.add_subplot(111)

    short_dates = [
        date[5:] for date in dates
    ]

    axis.plot(
        short_dates,
        min_temperatures,
        marker="o",
        linewidth=2,
        label="Min Temperature"
    )

    axis.plot(
        short_dates,
        max_temperatures,
        marker="o",
        linewidth=2,
        label="Max Temperature"
    )

    axis.set_title(
        f"Temperature Trend - {city}",
        fontsize=12,
        fontweight="bold"
    )

    axis.set_xlabel(
        "Date"
    )

    axis.set_ylabel(
        "Temperature (°C)"
    )

    axis.legend()

    axis.grid(
        True,
        alpha=0.25
    )

    figure.tight_layout()

    chart = FigureCanvasTkAgg(
        figure,
        master=chart_frame
    )

    chart.draw()

    chart.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ---------------- DARK/LIGHT MODE ----------------

def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        theme = dark_theme

        theme_button.config(
            text="☀️ Light Mode"
        )

    else:

        theme = light_theme

        theme_button.config(
            text="🌙 Dark Mode"
        )

    window.config(
        bg=theme["bg"]
    )

    canvas.config(
        bg=theme["bg"]
    )

    container.config(
        bg=theme["bg"]
    )

    main_frame.config(
        bg=theme["bg"]
    )

    for widget in [
        title_label,
        subtitle_label,
        current_label,
        advice_label,
        forecast_label,
        chart_label
    ]:

        widget.config(
            bg=theme["bg"],
            fg=theme["text"]
        )

    search_frame.config(
        bg=theme["bg"]
    )

    city_entry.config(
        bg=theme["card"],
        fg=theme["text"],
        insertbackground=theme["text"]
    )

    for card in [
        weather_card,
        advice_card,
        forecast_card,
        chart_frame
    ]:

        card.config(
            bg=theme["card"]
        )

    result_label.config(
        bg=theme["card"],
        fg=theme["text"]
    )

    advice_result.config(
        bg=theme["card"],
        fg=theme["text"]
    )

    forecast_result.config(
        bg=theme["card"],
        fg=theme["text"]
    )

    search_button.config(
        bg=theme["button"],
        fg=theme["text"],
        activebackground=theme["button"]
    )

    refresh_button.config(
        bg=theme["button"],
        fg=theme["text"],
        activebackground=theme["button"]
    )

    theme_button.config(
        bg=theme["button"],
        fg=theme["text"],
        activebackground=theme["button"]
    )


# ---------------- MAIN WINDOW ----------------

window = tk.Tk()

window.title(
    "Python Weather App"
)

window.geometry(
    "900x750"
)

window.minsize(
    700,
    600
)

window.resizable(
    True,
    True
)


# ---------------- SCROLLABLE AREA ----------------

container = tk.Frame(
    window
)

container.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    container,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# ---------------- CONTENT FRAME ----------------

main_frame = tk.Frame(
    canvas,
    padx=35,
    pady=25
)

canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)


def resize_content(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_content
)


def mouse_scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# ---------------- HEADER ----------------

title_label = tk.Label(
    main_frame,
    text="🌤 PYTHON WEATHER APP",
    font=("Arial", 26, "bold")
)

title_label.pack(
    pady=(5, 3)
)


subtitle_label = tk.Label(
    main_frame,
    text="Real-Time Weather • 5-Day Forecast • Temperature Analysis",
    font=("Arial", 11)
)

subtitle_label.pack(
    pady=(0, 18)
)


# ---------------- THEME BUTTON ----------------

theme_button = tk.Button(
    main_frame,
    text="🌙 Dark Mode",
    font=("Arial", 10, "bold"),
    padx=16,
    pady=6,
    relief="flat",
    cursor="hand2",
    command=toggle_theme
)

theme_button.pack(
    pady=(0, 18)
)


# ---------------- SEARCH ----------------

search_frame = tk.Frame(
    main_frame
)

search_frame.pack(
    pady=5
)


city_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 14),
    relief="solid",
    bd=1
)

city_entry.grid(
    row=0,
    column=0,
    padx=6
)

city_entry.insert(
    0,
    "Bangalore"
)

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.grid(
    row=0,
    column=1,
    padx=6
)


# ---------------- REFRESH ----------------

refresh_button = tk.Button(
    main_frame,
    text="🔄 Refresh Weather",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=6,
    relief="flat",
    cursor="hand2",
    command=refresh_weather
)

refresh_button.pack(
    pady=(12, 5)
)


# ---------------- CURRENT WEATHER ----------------

current_label = tk.Label(
    main_frame,
    text="CURRENT WEATHER",
    font=("Arial", 17, "bold")
)

current_label.pack(
    pady=(20, 8)
)


weather_card = tk.Frame(
    main_frame,
    bd=1,
    relief="solid",
    padx=25,
    pady=22
)

weather_card.pack(
    fill="x",
    pady=5
)


result_text = tk.StringVar()

result_label = tk.Label(
    weather_card,
    textvariable=result_text,
    font=("Arial", 12),
    justify="left"
)

result_label.pack()


# ---------------- ADVICE ----------------

advice_label = tk.Label(
    main_frame,
    text="WEATHER ADVICE",
    font=("Arial", 17, "bold")
)

advice_label.pack(
    pady=(22, 8)
)


advice_card = tk.Frame(
    main_frame,
    bd=1,
    relief="solid",
    padx=25,
    pady=18
)

advice_card.pack(
    fill="x",
    pady=5
)


advice_text = tk.StringVar()

advice_result = tk.Label(
    advice_card,
    textvariable=advice_text,
    font=("Arial", 11),
    justify="left",
    wraplength=750
)

advice_result.pack()


# ---------------- FORECAST ----------------

forecast_label = tk.Label(
    main_frame,
    text="5-DAY FORECAST",
    font=("Arial", 17, "bold")
)

forecast_label.pack(
    pady=(22, 8)
)


forecast_card = tk.Frame(
    main_frame,
    bd=1,
    relief="solid",
    padx=25,
    pady=18
)

forecast_card.pack(
    fill="x",
    pady=5
)


forecast_text = tk.StringVar()

forecast_result = tk.Label(
    forecast_card,
    textvariable=forecast_text,
    font=("Arial", 11),
    justify="left"
)

forecast_result.pack()


# ---------------- CHART ----------------

chart_label = tk.Label(
    main_frame,
    text="TEMPERATURE TREND",
    font=("Arial", 17, "bold")
)

chart_label.pack(
    pady=(22, 8)
)


chart_frame = tk.Frame(
    main_frame,
    bd=1,
    relief="solid",
    padx=10,
    pady=10,
    height=380
)

chart_frame.pack(
    fill="x",
    pady=(5, 25)
)

chart_frame.pack_propagate(
    False
)


# ---------------- INITIAL THEME ----------------

toggle_theme()
toggle_theme()


# ---------------- START APPLICATION ----------------

window.mainloop()