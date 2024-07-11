import os
import time
from datetime import date

import pandas as pd
import requests
from dotenv import load_dotenv


def fetch_weather_data(lat: float, lon: float, start_time: str, end_time: str, api_key: str) -> list:
    url = r"https://history.openweathermap.org/data/2.5/history/city?"

    parameters = {
        "lat": lat,
        "lon": lon,
        "type": "hour",
        #"start": start_time,
        #"end": end_time,
        "appid": api_key
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        return data['list']
    else:
        print(f"Error fetching data: {response.status_code}")
        return []


def save_to_csv(weather: list, output_file: str):
    if weather:
        df = pd.DataFrame(weather)
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")


if __name__ == "__main__":
    # Specify the output file path
    output_file = 'weather_data.csv'

    # Specify the weather coordinates (for Boston)
    lat = 42.3554334
    lon = -71.060511

    # Specify the start and end dates for the weather data (UNIX timestamps)
    start_time = date.today().replace(year=date.today().year - 1)
    end_time = date.today()

    print(f"Fetching weather data from {start_time} to {end_time}")

    start_time = str(int(time.mktime(start_time.timetuple())))
    end_time = str(int(time.mktime(end_time.timetuple())))

    # Get the API key from the environment variable
    load_dotenv()
    api_key: str = os.getenv('weatherAPI')

    # Fetch the weather data
    weather = fetch_weather_data(lat, lon, start_time, end_time, api_key)

    # Save the data to a CSV file
    save_to_csv(weather, output_file)

# %%
