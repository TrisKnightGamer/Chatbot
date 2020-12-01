from requests import get
from ip2geotools.databases.noncommercial import DbIpCity
import requests, json
from geopy.geocoders import Nominatim
import json
from underthesea import word_tokenize

geolocator = Nominatim(user_agent="Chatbot")

def weather(content, is_general=True):
    try:
        content.lower()
        location_districts_name = ""
        location_name_city = ""
        place = ""
        sentence = word_tokenize(content)
        for i in sentence:
            content = i
            content.replace('_', ' ')
            content.lower()
            with open('/app/backend/NLP/data/location.json', encoding="utf8") as f:
                data = json.load(f)
                main = data['main']
                length = len(main)
                for z in range(length):
                    name_city = main[z]['name']   
                    name_city.lower()
                    districts = main[z]['districts']
                    length_1 = len(districts)
                    for x in range(length_1):
                        districts_name = districts[x]['name']
                        districts_name.lower()
                        if( name_city.find(content) != -1 ):
                            location_name_city = name_city
                            break
                        if( districts_name.find(content) != -1 ):
                            location_districts_name = districts_name
                            break
        place = location_districts_name + ", " + location_name_city
        location = geolocator.geocode(str(place))
        print(place)
        lng = str(location.longitude)
        lat = str(location.latitude)

        BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
        API_KEY = "4e10bd9c2a268325e6ed167bd2ac57be"

        URL = BASE_URL + "lat=" + lat + "&lon=" + lng + "&units=metric&exclude=daily&appid=" + API_KEY
        response = requests.get(URL)
        print(URL)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            ################# Get weather current #############################
            # getting the main dict block
            current = data['current']
            # getting temperature
            temperature = current['temp']
            print(type(temperature))
            # getting temperature feel like 
            feels_like = current['feels_like']
            # getting the humidity
            humidity = current['humidity']
            # getting the wind_speed
            wind_speed = current['wind_speed']

            ################# Get weather forecast for 48 hours #############################
            # getting the main dict block
            hourly = data['hourly']
            # getting temperature
            temperature_48 = hourly[1]['temp']
            # getting temperature feel like 
            feels_like_48 = hourly[1]['feels_like']
            # getting the humidity
            humidity_48 = hourly[1]['humidity']
            # getting the wind_speed
            wind_speed_48 = hourly[1]['wind_speed']

            #######################################################################
            print(f"Thời tiết tại : {content} ")
            print(f"Thời tiết hiện tại :")
            print(f"    Nhiệt độ: {temperature} °C")
            print(f"    Cảm thấy như là : {feels_like} °C")
            print(f"    Độ ẩm: {humidity}%")
            print(f"    Tốc độ gió: {wind_speed}km/h")
            print(f"Thời tiết trong 48 tiếng tới :")
            print(f"    Nhiệt độ: {temperature_48} °C")
            print(f"    Cảm thấy như là : {feels_like_48} °C")
            print(f"    Độ ẩm: {humidity_48}%")
            print(f"    Tốc độ gió: {wind_speed_48}km/h")
            res = f"Thời tiết tại : {location}\n" + f"Thời tiết hiện tại :\n" + f"    Nhiệt độ: {temperature}°C\n" + f"    Cảm thấy như là : {feels_like}°C\n" + f"    Độ ẩm: {humidity}%\n" + f"    Tốc độ gió: {wind_speed}m/s\n" #+ f"Thời tiết trong 48 tiếng tới :\n" + f"    Nhiệt độ: {temperature_48}°C\n" + f"    Cảm thấy như là : {feels_like_48}°C\n" + f"    Độ ẩm: {humidity_48}%\n" + f"    Tốc độ gió: {wind_speed_48}m/s\n"
            return {
                    "result": res
                }
        else:
            # showing the error message
            print("Error in the HTTP request")
            return {
                "result": False
            }   
    except:
        print("Exception cause error !")
        content.replace(districts_name + ', ', '')
        return {
            "result" : str(process_exception(content, is_general=True))
        }

def process_exception(content, is_general=True):
    try:
        content.lower()
        location_name_city = ""
        place = ""
        sentence = word_tokenize(content)
        for i in sentence:
            content = i
            content.replace('_', ' ')
            content.lower()
            with open('C:/Users/Trihd/OneDrive/chatbot_NEW/backend/NLP/data/location.json', encoding="utf8") as f:
                data = json.load(f)
                main = data['main']
                length = len(main)
                for z in range(length):
                    name_city = main[z]['name']   
                    name_city.lower()
                    if( name_city.find(content) != -1 ):
                        location_name_city = name_city
                        break
        place = location_name_city
        location = geolocator.geocode(str(place))
        print(place)
        lng = str(location.longitude)
        lat = str(location.latitude)

        BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
        API_KEY = "4e10bd9c2a268325e6ed167bd2ac57be"

        URL = BASE_URL + "lat=" + lat + "&lon=" + lng + "&units=metric&exclude=daily&appid=" + API_KEY
        response = requests.get(URL)
        print(URL)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            ################# Get weather current #############################
            # getting the main dict block
            current = data['current']
            # getting temperature
            temperature = current['temp']
            print(type(temperature))
            # getting temperature feel like 
            feels_like = current['feels_like']
            # getting the humidity
            humidity = current['humidity']
            # getting the wind_speed
            wind_speed = current['wind_speed']

            ################# Get weather forecast for 48 hours #############################
            # getting the main dict block
            hourly = data['hourly']
            # getting temperature
            temperature_48 = hourly[1]['temp']
            # getting temperature feel like 
            feels_like_48 = hourly[1]['feels_like']
            # getting the humidity
            humidity_48 = hourly[1]['humidity']
            # getting the wind_speed
            wind_speed_48 = hourly[1]['wind_speed']

            #######################################################################
            print(f"Thời tiết tại : {content} ")
            print(f"Thời tiết hiện tại :")
            print(f"    Nhiệt độ: {temperature} °C")
            print(f"    Cảm thấy như là : {feels_like} °C")
            print(f"    Độ ẩm: {humidity}%")
            print(f"    Tốc độ gió: {wind_speed}km/h")
            print(f"Thời tiết trong 48 tiếng tới :")
            print(f"    Nhiệt độ: {temperature_48} °C")
            print(f"    Cảm thấy như là : {feels_like_48} °C")
            print(f"    Độ ẩm: {humidity_48}%")
            print(f"    Tốc độ gió: {wind_speed_48}km/h")
            res = f"Thời tiết tại : {location}\n" + f"Thời tiết hiện tại :\n" + f"    Nhiệt độ: {temperature}°C\n" + f"    Cảm thấy như là : {feels_like}°C\n" + f"    Độ ẩm: {humidity}%\n" + f"    Tốc độ gió: {wind_speed}m/s\n" #+ f"Thời tiết trong 48 tiếng tới :\n" + f"    Nhiệt độ: {temperature_48}°C\n" + f"    Cảm thấy như là : {feels_like_48}°C\n" + f"    Độ ẩm: {humidity_48}%\n" + f"    Tốc độ gió: {wind_speed_48}m/s\n"
            return res
        else:
            # showing the error message
            print("Error in the HTTP request")
            return False
    except:
        print("Exception cause error !")
        return False
# if __name__ == '__main__':
#     weather("hải châu, đà nẵng", is_general=True)