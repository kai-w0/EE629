Project: Weather Reporting System
===
By the project I want to design a weather reporting system. It can remind you of the weather condition and give you some advice about cloth after you get up every day.
## module
```urllib.request```to get weather information.
```playsound```to broadcast.
```baidu-aip```to change txt to sound.
## implement
I use baidu-aip to achive smart text conversion. Baidu-aip provide us free api and SDK. It can convert txt to mp3.
```
pip install baidu-aip
```
to install the module.
After installing, we need to register a baiduAI account to get key. 
For weather information, we get it from [weather](http://apis.juhe.cn/simpleWeather).
