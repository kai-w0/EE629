# Weather Voice Broadcast
# 1. Enter city
# 2. Send request for api to get weather information
# 3. Filter information, select what you need, and process
# 4. Use baiduAI to get mp3 file
# 5. Broadcast information

# modules
import requests                                     # send request
from aip import AipSpeech                           # transform text to mp3
from playsound import playsound                     # broadcast
from setting import APP_ID, API_KEY, SECRET_KEY     # get key to use SDK
import os, sys                                      # clean files

# Send request for api to get weather information
def getWeather_infor(city):

    url = "http://apis.juhe.cn/simpleWeather/query?"    # url
    params = {                                          # parameters
        "city": city,
        "key": "a1967d854996051f711fd48a456b6c1e"
    }
    resp = requests.get(url, params=params).json()       # use json() to get dict
    return  resp


# Filter information, select what you need, and process
def select_info(resp):
    if resp["result"]:  # successfully request
        realtime_Weather = resp["result"]["realtime"]           # current temperature
        day_Weather = resp["result"]["future"][0]               # weather condition
        temp = day_Weather["temperature"].split("/")            # split highest and lowest temperature
        speak_content = f'Current temperature is{realtime_Weather["temperature"]}℃,relative humidity is{realtime_Weather["humidity"]}%' \
                        f',the weather is：{realtime_Weather["info"]},{realtime_Weather["direct"]},' \
                        f'the power of wind is：{realtime_Weather["power"]}。\n' \
                        f'the range of temperature is：{temp[0]}--{temp[1]}，weather condition is：{day_Weather["weather"]}'
    else:
        speak_content = resp["reason"]
    return speak_content


# get mp3 file
def create_Mp3(content):

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)            # request for online client
    result = client.synthesis(content, 'zh', 1, {'spd':6,'vol': 5})  # get the binary file stream

    if not isinstance(result, dict):              # Recognize correctly then return speech binary, else return dict
        with open('auido.mp3', 'wb') as f:
            f.write(result)

def cleanMp3():
    if (os.path.exists("auido.mp3")):
        os.remove("auido.mp3")


# main
if __name__=="__main__":

    print("-"*20,"Weather broadcast program","-"*20)

    while True:
        city = input("\nPlease enter the city(or enter exit):")
        if city != 'exit':
            resp = getWeather_infor(city)
            we_con = select_info(resp)
            create_Mp3(we_con)
            print(we_con)
            playsound('auido.mp3')
        else:
            print("Program exit")
            break

    #  Clean up voice files after the program exits
    cleanMp3()





















