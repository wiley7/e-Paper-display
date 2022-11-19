# coding=utf-8

import requests
import re
KEY = "cd79a7c9ab124e4c8c22da88ccfdd846"
APIURL = "https://devapi.qweather.com/v7/weather"
LOCATION = "101010100"
s = requests.session()
import logging
import argparse
import json
logging.basicConfig(level=logging.DEBUG)

def api_url(api_type):
    return "{}/{}?location={}&key={}".format(APIURL,api_type,LOCATION,KEY)

# 实况天气
def now():
    api_type = "now"
    # url = https://devapi.qweather.com/v7/weather/now?location=101010100&key=cd79a7c9ab124e4c8c22da88ccfdd846
    url = api_url(api_type)
    raw_json = s.get(url).json()
    if raw_json["code"] != "200":
        logging.error("api return error: %s", json.dumps(raw_json))
        return
    now_now = raw_json["now"]
    now_tmp = now_now["temp"]  # 实时气温
    now_cond = now_now["text"]  # 天气描述
    now_fl = now_now["feelsLike"]  # 体感温度
    now_sc = now_now["windScale"]  # 风力级别
    text = "天气 {}, {}°, 体感 {}°, 风力 {}".format(now_cond, now_tmp, now_fl, now_sc)
    return text

# 三天气
def daily():
    api_type = "3d"
    # url = https://devapi.qweather.com/v7/weather/3d?location=101010100&key=cd79a7c9ab124e4c8c22da88ccfdd846
    url = api_url(api_type)
    raw_json = s.get(url).json()
    if raw_json["code"] != "200":
        logging.error("api return error: %s", json.dumps(raw_json))
        return
    output = ""
    for daily in raw_json["daily"]:
        text = "{}: {}, {} ~ {}°, {} {}级".format(daily["fxDate"], daily["textDay"], daily["tempMin"], daily["tempMax"], daily["windDirDay"], daily["windScaleDay"])
        output = output + "\n" + text
    return output


if __name__ == '__main__':
    print(daily())