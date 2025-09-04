# Weather Dashboard

A simple Django application that displays the current weather for a searched city using the OpenWeatherMap API.

## Features

- Real-time weather data fetching.
- Autocomplete city search for the top 1000 most populated cities.
- Clean and simple user interface.

## Setup and Installation

1.  **Clone the repository:**
    `git clone <your-repo-url>`
2.  **Create a virtual environment:**
    `python -m venv venv`
    `source venv/bin/activate`
3.  **Install dependencies:**
    `pip install -r requirements.txt`
4.  **Create a `.env` file** in the root directory and add your API key:
    `OPENWEATHER_API_KEY='your_actual_api_key'`
5.  **Run migrations:**
    `python manage.py migrate`
6.  **Start the development server:**
    `python manage.py runserver`