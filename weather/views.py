import requests
from django.shortcuts import render
from decouple import config

# Replace 'Your_API_Key' with your actual WeatherAPI.com API key
API_KEY = config('WEATHER_API')

def get_weather_data(city_name):
    current_weather_url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_name}&aqi=yes'
    forecast_url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=3'
    
    current_weather_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)
    
    # print(current_weather_response)
    # print(forecast_response)
    
    if current_weather_response.status_code == 200 and forecast_response.status_code == 200:
        current_weather_data = current_weather_response.json()
        # print(current_weather_data)
        
        forecast_data = forecast_response.json()
        return current_weather_data, forecast_data
    else: 
        # Handle errors 
        return None, None

def index(request):
    default_city_name = 'Pokhara'  # Replace with the method to get the device's location
    weather_data, forecast_data = get_weather_data(default_city_name)

    if request.method == 'POST':
        city_name = request.POST.get('city')
        search_weather_data, search_forecast_data = get_weather_data(city_name)
        context = {
            'weather_data': weather_data,
            'forecast_data': forecast_data,
            'search_weather_data': search_weather_data,
            'search_forecast_data': search_forecast_data,
            'city': city_name,
        }
    else:
        context = {
            'weather_data': weather_data,
            'forecast_data': forecast_data,
        }

    return render(request, 'index.html', context)







# from django.shortcuts import render
# import requests

# # Replace 'Your_API_Key' with your actual OpenWeatherMap API key
# API_KEY = 'WEATHER_API'

# def get_weather_by_city(city_name):
#     response = requests.get(
#         f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}')
#     return response.json()


# def index(request):
#     default_city_name = 'Kathmandu'  # Replace with the method to get the device's location
#     weather_data = get_weather_by_city(default_city_name)
#     forecast_data = get_3_day_forecast(default_city_name)

#     if request.method == 'POST':
#         city_name = request.POST.get('city')
#         search_weather_data = get_weather_by_city(city_name)
#         search_forecast_data = get_3_day_forecast(city_name)
#         context = {
#             'weather_data': weather_data,
#             'forecast_data': forecast_data,
#             'search_weather_data': search_weather_data,
#             'search_forecast_data': search_forecast_data,
#             'city': city_name,
#         }
#     else:
#         context = {
#             'weather_data': weather_data,
#             'forecast_data': forecast_data,
#         }

#     return render(request, 'index.html', context)


# from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
# from decouple import config
# import datetime
# import requests
# from django.shortcuts import render


# def get_3_day_forecast(city_name):
#     response = requests.get(
#         f'http://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt=3&appid={API_KEY}')
#     return response.json()

# def index(request):
#     default_city_name = 'Kathmandu'  # Replace with the method to get the device's location
#     weather_data = get_weather_by_city(default_city_name)
#     forecast_data = get_3_day_forecast(default_city_name)

#     if request.method == 'POST':
#         city_name = request.POST.get('city')
#         search_weather_data = get_weather_by_city(city_name)
#         search_forecast_data = get_3_day_forecast(city_name)
#         context = {
#             'weather_data': weather_data,
#             'forecast_data': forecast_data,
#             'search_weather_data': search_weather_data,
#             'search_forecast_data': search_forecast_data,
#             'city': city_name,
#         }
#     else:
#         context = {
#             'weather_data': weather_data,
#             'forecast_data': forecast_data,
#         }

#     return render(request, 'index.html', context)


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip



# api_key = config('WEATHER_API')

# def index(request):
#     user_ip = get_client_ip(request)
#     g = GeoIP2()
    
#     # Get the user's location
#     user_location = g.city(user_ip)
#     default_city_name = user_location['city']
#     print(default_city_name)
    
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

#     if request.method == 'POST':
#         city1 = request.POST['city1']
#         city2 = request.POST.get('city2', None)

#         weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

#         if city2:
#             weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
#                                                                          forecast_url)
#         else:
#             weather_data2, daily_forecasts2 = None, None

#         context = {
#             'weather_data1': weather_data1,
#             'daily_forecasts1': daily_forecasts1,
#             'weather_data2': weather_data2,
#             'daily_forecasts2': daily_forecasts2,
#         }

#         return render(request, 'weather/index.html', context)
#     else:
#         return render(request, 'weather/index.html')


# def get_3_day_forecast(city_name):
#     response = requests.get(
#         f'http://api.openweathermap.org/data/2.5/forecast/daily?q={city_name}&cnt=3&appid={api_key}')
#     return response.json()

# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     response = requests.get(current_weather_url.format(city, api_key)).json()
#     lat, lon = response['coord']['lat'], response['coord']['lon']
#     forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
#     print(forecast_response)
    
    

#     weather_data = {
#         'city': city,
#         'temperature': round(response['main']['temp'] - 273.15, 2),
#         'description': response['weather'][0]['description'],
#         'icon': response['weather'][0]['icon'],
#     }
    


#     daily_forecasts = []
    
#     forecast_data = get_3_day_forecast(city_name=city)
#     print(forecast_data)
    
#     # for daily_data in forecast_response['daily'][:5]:
#     #     daily_forecasts.append({
#     #         'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#     #         'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#     #         'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#     #         'description': daily_data['weather'][0]['description'],
#     #         'icon': daily_data['weather'][0]['icon'],
#     #     })

#     return weather_data, daily_forecasts