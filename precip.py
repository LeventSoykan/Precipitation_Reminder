import os
import requests
import json
import smtplib, ssl
import email.message
from datetime import datetime, timedelta


def get_forecast(latitude, longitude, api_key):
    source = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}')
    forecast_json = json.loads(source.text)
    rain_today = False
    rain_tomorrow = False
    forecast = '\nTODAY\n'
    for day in forecast_json['list']:
        day_datetime = datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if day_datetime.date() == datetime.today().date():
            weather_desc = day['weather'][0]['description']
            forecast += f"Date: {day['dt_txt']} - Weather: {weather_desc}\n"
            rain_today = 'rain' in weather_desc
    forecast += '\nTOMORROW\n'
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    for day in forecast_json['list']:
        day_datetime = datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if day_datetime.date() == tomorrow:
            weather_desc = day['weather'][0]['description']
            forecast += f"Date: {day['dt_txt']} - Weather: {day['weather'][0]['description']}\n"
            rain_tomorrow = 'rain' in weather_desc
    message_detail = {
        'date': datetime.today().date(),
        'forecast': forecast,
        'rain_today' : rain_today,
        'rain_tomorrow': rain_tomorrow
    }
    return message_detail

def send_forecast_email(port, sender_email, password, receiver_email, message_detail):
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.zoho.eu", port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        m = email.message.Message()
        m['From'] = sender_email
        m['To'] = receiver_email
        today_alert = ''
        tomorrow_alert = ''
        if message_detail['rain_today']:
            today_alert += 'Rain Today'
        if message_detail['rain_tomorrow']:
            tomorrow_alert += 'Rain Tomorrow'
        m['Subject'] = f"Weather Forecast for {message_detail['date']}  {today_alert} {tomorrow_alert}"
        m.set_payload(message_detail['forecast'])
        server.sendmail(sender_email, receiver_email, m.as_string())

if __name__ == '__main__':
    api_key = os.environ.get('OPEN_WEATHER_API')
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    latitude = 40.911753
    longitude = 29.251945
    port = 587  # For SSL
    sender_email = "leventsoykan@zohomail.eu"
    receiver_email = "levent_soykan@yahoo.com"
    message_detail = get_forecast(latitude, longitude, api_key)
    send_forecast_email(port, sender_email, email_pass, receiver_email, message_detail)