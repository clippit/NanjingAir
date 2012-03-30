#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Convert PM 2.5 concentration to AQI
"""
from math import ceil
import abc


class AQI(object):
    """Convert PM 2.5 concentration to AQI"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, conc):
        self._conc = conc
        self.aqi = self.aqi_pm25(self._conc)
        self.aqi_desc = self.aqi_desc(self.aqi)

    def linear(self, aqi_high, aqi_low, conc_high, conc_low, conc):
        a = (aqi_high - aqi_low) / (conc_high - conc_low) * (conc - conc_low) + aqi_low
        return int(ceil(a))

    @abc.abstractmethod
    def aqi_pm25(self, c):
        return

    @abc.abstractmethod
    def aqi_desc(self, aqi):
        return

    def __call__(self):
        return self.aqi, self.aqi_desc


class AQIChina(AQI):
    """Based on HJ 633-2012 'Technical Regulation on Ambient Air Quality Index (on trial)'"""
    def __init__(self, conc):
        super(AQIChina, self).__init__(conc)

    def aqi_pm25(self, c):
        if c >= 0 and c < 35.5:
            return self.linear(50.0, 0.0, 35.4, 0, c)
        elif c >= 35.5 and c < 75.5:
            return self.linear(100.0, 51.0, 75.4, 35.5, c)
        elif c >= 75.5 and c < 115.5:
            return self.linear(150.0, 101.0, 115.4, 75.5, c)
        elif c >= 115.5 and c < 150.5:
            return self.linear(200.0, 151.0, 150.4, 115.5, c)
        elif c >= 150.5 and c < 250.5:
            return self.linear(300.0, 201.0, 250.4, 150.5, c)
        elif c >= 250.5 and c < 350.5:
            return self.linear(400.0, 301.0, 350.4, 250.5, c)
        elif c >= 350.5 and c < 500.5:
            return self.linear(500.0, 401.0, 500.4, 350.5, c)
        elif c is None:
            return u"暂无数据"
        else:
            return u"超出范围"

    def aqi_desc(self, aqi):
        if aqi <= 50:
            return u"优"
        elif aqi > 50 and aqi <= 100:
            return u"良"
        elif aqi > 100 and aqi <= 150:
            return u"轻度污染"
        elif aqi > 150 and aqi <= 200:
            return u"中度污染"
        elif aqi > 200 and aqi <= 300:
            return u"重度污染"
        elif aqi > 300:
            return u"严重污染"
        else:
            return "-"


class AQIUS(AQI):
    """Based on US EPA-454/B-09-001
       'Technical Assistance Document for the Reporting of Daily Air Quality
        – the Air Quality Index (AQI)'"""
    def __init__(self, conc):
        super(AQIUS, self).__init__(conc)

    def aqi_pm25(self, c):
        if c >= 0 and c < 15.5:
            return self.linear(50, 0, 15.4, 0, c)
        elif c >= 15.5 and c < 35.5:
            return self.linear(100, 51, 35.4, 15.5, c)
        elif c >= 35.5 and c < 65.5:
            return self.linear(150, 101, 65.4, 35.5, c)
        elif c >= 65.5 and c < 150.5:
            return self.linear(200, 151, 150.4, 65.5, c)
        elif c >= 150.5 and c < 250.5:
            return self.linear(300, 201, 250.4, 150.5, c)
        elif c >= 250.5 and c < 350.5:
            return self.linear(400, 301, 350.4, 250.5, c)
        elif c >= 350.5 and c < 500.5:
            return self.linear(500, 401, 500.4, 350.5, c)
        elif c is None:
            return u"暂无数据"
        else:
            return u"超出范围"

    def aqi_desc(self, aqi):
        if aqi <= 50:
            return u"优秀"
        elif aqi > 50 and aqi <= 100:
            return u"中等"
        elif aqi > 100 and aqi <= 150:
            return u"敏感人群有害"
        elif aqi > 150 and aqi <= 200:
            return u"不健康"
        elif aqi > 200 and aqi <= 300:
            return u"非常不健康"
        elif aqi > 300 and aqi <= 500:
            return u"有毒害危险"
        elif aqi == u"暂无数据":
            return "-"
        else:
            return u"悲剧……已爆表>_<"
