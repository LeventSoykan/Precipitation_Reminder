import os
import requests
import json


api_key = os.environ.get('OPEN_WEATHER_API')
latitude = 40.911753
longitude = 29.251945

source = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}')

forecast_json = json.loads(source.text)

forecast_str = json.dumps(forecast_json, indent=4, sort_keys=True)
print(forecast_str)
for day in forecast_json['list']:
    print(f"Date: {day['dt_txt']} - Weather: {day['weather'][0]['description']}")