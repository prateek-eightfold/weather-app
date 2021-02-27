import json
import requests

WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
ICON_BASE_URL = 'https://bmcdn.nl/assets/weather-icons/all/'

ICONS = {
    '01d' : 'clear-day.svg',
    '01n' : 'clear-night.svg',
    '02d' : 'partly-cloudy-day.svg',
    '02n' : 'partly-cloudy-night.svg',
    '03d' : 'cloudy.svg',
    '03n' : 'cloudy.svg',
    '04d' : 'overcast.svg',
    '04n' : 'overcast.svg',
    '09d' : 'drizzle.svg',
    '09n' : 'drizzle.svg',
    '10d' : 'rain.svg',
    '10n' : 'rain.svg',
    '11d' : 'thunderstorms.svg',
    '11n' : 'thunderstorms.svg',
    '13d' : 'snow.svg',
    '13n' : 'snow.svg',
    '50d' : 'mist.svg',
    '50n' : 'mist.svg'
}

def get_icon_url(icon_key):
    return ICON_BASE_URL + ICONS.get(icon_key, '01d')

def return_error_template():
    data = {
        'title': 'Weather',
        'error': 'Unable to find city for weather information.',
        'logo_url': get_icon_url('01d')
    }

    return {
        'statusCode': 200,
        'body': json.dumps({'data': data})
    }

def career_hub_profile_view_handler(event, context):
    payload = json.loads(event.get('body')) if event.get('body') else {}
    req_data = payload.get('request_data', {})
    app_settings = payload.get('app_settings', {})


    api_key = 'c39f66947525ebb7dca5b03410f5a503'
    location = req_data.get('location')
    location_country_code = req_data.get('location_country_code', '')
    if not location:
        return return_error_template()

    city = '{}, {}'.format(location, location_country_code) if location_country_code and location.count(',') <= 1 else location.split(',')[0]
    temp_units = app_settings.get('temperature_units', 'F')
    temp_units_api = 'imperial' if temp_units == 'F' else 'metric'
    payload = {'appid' : api_key, 'q': city, 'units': temp_units_api}
    resp = requests.get(WEATHER_URL, params=payload)
    json_resp = resp.json()

    temp = json_resp.get('main', {}).get('temp', None)
    if temp is None:
        return return_error_template()

    temp = round(float(temp), 1)

    weather_data = json_resp.get('weather', [{}])[0]
    if not weather_data:
        return return_error_template()

    icon_url = get_icon_url(weather_data.get('icon'))
    condition = weather_data.get('description', '')
    condition = ' '.join(word.capitalize() for word in condition.split())

    data = {
        'title': u'{}\u00b0{} - {}'.format(temp, temp_units, condition),
        'subtitle': location,
        'logo_url': icon_url
    }
    return {
        'statusCode': 200,
        'body': json.dumps({'data': data})
    }