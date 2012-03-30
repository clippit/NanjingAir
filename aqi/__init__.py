#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Convert PM 2.5 concentration to AQI
Thanks to James Chen: http://imtx.me/archives/1704.html
"""


def linear(aqi_high, aqi_low, conc_high, conc_low, conc):
    a = ((conc - conc_low) / (conc_high - conc_low)) * (aqi_high - aqi_low) + aqi_low
    return int(round(a))


def aqi_pm25(c):
    if c >= 0 and c < 15.5:
        return linear(50, 0, 15.4, 0, c)
    elif c >= 15.5 and c < 35.5:
        return linear(100, 51, 35.4, 15.5, c)
    elif c >= 35.5 and c < 65.5:
        return linear(150, 101, 65.4, 35.5, c)
    elif c >= 65.5 and c < 150.5:
        return linear(200, 151, 150.4, 65.5, c)
    elif c >= 150.5 and c < 250.5:
        return linear(300, 201, 250.4, 150.5, c)
    elif c >= 250.5 and c < 350.5:
        return linear(400, 301, 350.4, 250.5, c)
    elif c >= 350.5 and c < 500.5:
        return linear(500, 401, 500.4, 350.5, c)
    elif c is None:
        return u"暂无数据"
    else:
        return u"超出范围"


def aqi_desc(aqi):
    if aqi <= 50:
        return u"优良"
    elif aqi > 50 and aqi <= 100:
        return u"中等"
    elif aqi > 100 and aqi <= 150:
        return u"敏感群体有害"
    elif aqi > 150 and aqi <= 200:
        return u"不健康"
    elif aqi > 200 and aqi <= 300:
        return u"非常不健康"
    elif aqi > 300 and aqi <= 400:
        return u"有毒害一级"
    elif aqi > 400 and aqi <= 500:
        return u"有毒害二级"
    elif aqi == u"暂无数据":
        return "-"
    else:
        return u"悲剧……已爆表>_<"
