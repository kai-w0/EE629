import urllib.parse
import urllib.request
import gzip
import json
import playsound
from aip import AipSpeech
import matplotlib.pyplot as plt
import re
import pygame
#设置参数，图片显示中文字符，否则乱码
plt.rcParams['font.sans-serif']=['SimHei']

# 播放天气和音乐
def py_game_player(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=1, start=0.0)
    print("播放音乐")
    while True:
        if pygame.mixer.music.get_busy() == 0:
            # Linux 配置定时任务要设置绝对路径
            mp3 = "G:/files/leetcode/"+str(random.randint(1, 6)) + ".mp3"
            # mp3 = str(random.randint(1, 6)) + ".mp3"
            pygame.mixer.music.load(mp3)
            pygame.mixer.music.play(loops=1, start=0.0)
            break
    while True:
        if pygame.mixer.music.get_busy() == 0:
            print("播报完毕，起床啦")
            break

#定义获取天气数据函数
def Get_weather_data():
    print('------天气查询------')
    city_name = input('请输入要查询的城市名称：')
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city_name)
    weather_data = urllib.request.urlopen(url).read()
    # 读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    # #解压网页数据
    weather_dict = json.loads(weather_data)
    return weather_dict
#定义当天天气输出格式
def Show_weather(weather_data):
    weather_dict = weather_data
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市有误或未收录天气，请重新输入...')
    elif weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
        print('日期：', forecast[0].get('date'))
        print('城市：', weather_dict.get('data').get('city'))
        print('天气：', forecast[0].get('type'))
        print('温度：', weather_dict.get('data').get('wendu') + '℃ ')
        print('高温：', forecast[0].get('high'))
        print('低温：', forecast[0].get('low'))
        #print('风级：', forecast[0].get('fengli').split('<')[2].split(']')[0])
        print('风向：', forecast[0].get('fengxiang'))
        weather_forecast_txt = '您好，您所在的城市%s,' \
                               '天气%s,' \
                               '当前温度%s，' \
                               '今天最高温度%s，' \
                               '最低温度%s，' \
                               '温馨提示：%s' % \
                               (
                                   weather_dict.get('data').get('city'),
                                   forecast[0].get('type'),
                                   weather_dict.get('data').get('wendu'),
                                   forecast[0].get('high'),
                                   forecast[0].get('low'),

                                   weather_dict.get('data').get('ganmao')
                               )
        return weather_forecast_txt,forecast
#定义语音播报今天天气状况
def Voice_broadcast(weather_forcast_txt):
    weather_forecast_txt = weather_forcast_txt
    APP_ID = '23092640'
    API_KEY = 'cGIZyHHzZDnPvr2Dv9KF2fAc'
    SECRET_KEY = 'z284ht1uP4QfkkQ584mlVqKq3m13YiG3'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    print('语音提醒：', weather_forecast_txt)
    #百度语音合成
    result = client.synthesis(weather_forecast_txt, 'zh', 1, {'vol': 5})
    if not isinstance(result, dict):
        with open('audio2.mp3', 'wb') as f:
            f.write(result)
            f.close()
    #playsound模块播放语音
    playsound.playsound('audio2.mp3')

if __name__=='__main__':
    weather_data = Get_weather_data()
    weather_forecast_txt, forecast = Show_weather(weather_data)
    py_game_player(file)
    Voice_broadcast(weather_forecast_txt)