# 🌦️ Weather App

A simple Python weather application that allows users to check the current weather of any city using a weather API.

## ✨ Features

* Search weather by city
* Displays temperature, weather condition, humidity, wind speed, and pressure
* Shows a weather trend graph for easy visualization
* Handles invalid city names and API errors
* Keeps the API key secure using a `.env` file

## 🛠️ Built With

* Python
* Requests
* Weather API
* JSON
* python-dotenv
* Matplotlib

## 🔄 How It Works

The user enters a city → Python sends a request to the weather API → the JSON response is processed → weather details and the trend graph are displayed.

## ▶️ How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your API key:

```text
OPENWEATHER_API_KEY=your_api_key_here
```

Then run:

```bash
python main.py
```

## 📚 What I Learned

This project helped me gain hands-on experience with **API integration, JSON data, error handling, environment variables, and data visualization** while building a practical Python application.

## 👩‍💻 Author

**Ankitha SA**
ECE Engineering Student | Python & C | DSA | Machine Learning
