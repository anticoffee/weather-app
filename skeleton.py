import requests
from datetime import datetime

api_key = 'd3bf16237ddb9fe0105eb06d591846d8'

location = input("Enter a city:")

url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial&appid={api_key}'
results = requests.get(url)

if results.status_code == 404:
       print('City was not found')
else:
    city = results.json()['name']
    country = results.json()['sys']['country']
    description = results.json()['weather'][0]['description']
    temp = round(results.json()['main']['temp'])
    low = round(results.json()['main']['temp_min'])
    high = round(results.json()['main']['temp_max'])
    date = datetime.utcfromtimestamp(results.json()['dt'] + results.json()['timezone'])
    
    print(date)
    print(f'The weather in {city},{country} is {temp}°F with {description}')
    print(f'The highest being {high}°F and the lowest being {low}°F')
