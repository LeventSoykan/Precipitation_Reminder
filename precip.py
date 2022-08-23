import os
import requests
import json
import smtplib, ssl
import email.message


def get_forecast(latitude, longitude, api_key):
    source = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}')
    forecast_json = json.loads(source.text)
    forecast = ''
    for day in forecast_json['list']:
        forecast += f"Date: {day['dt_txt']} - Weather: {day['weather'][0]['description']}\n"
    return forecast

def send_forecast_email(port, sender_email, password, receiver_email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        m = email.message.Message()
        m['From'] = sender_email
        m['To'] = receiver_email
        m['Subject'] = "Weather Forecast"
        m.set_payload(message)
        server.sendmail(sender_email, receiver_email, m.as_string())

if __name__ == '__main__':
    api_key = os.environ.get('OPEN_WEATHER_API')
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    latitude = 40.911753
    longitude = 29.251945
    port = 587  # For SSL
    sender_email = "leventsoykan83@gmail.com"
    receiver_email = "levent_soykan@yahoo.com"
    message= get_forecast(latitude, longitude, api_key)
    send_forecast_email(port, sender_email, gmail_pass, receiver_email, message)