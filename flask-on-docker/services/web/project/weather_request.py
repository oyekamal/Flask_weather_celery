import requests


def get_weather_by_city(city="Islamabad"):
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a4cf48b5fa7319d2ffb2ffc7a5f0d438"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    
    return response.json()


if __name__ == '__main__':
    data = get_weather_by_city()
    print(data)