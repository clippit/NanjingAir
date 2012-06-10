#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
from base64 import b64decode
import pyDes
from pyamf.remoting.client import RemotingService
import config
from aqi import AQIChina, AQIUS
from social import update


def read_pm25():
    service = RemotingService(config.AMF_GATEWAY).getService('FlashRemotingServiceLibrary.Sample.getSurvyValue')
    extract = lambda s: int(s[8: s.find(u'微克')]) if s[9] != u'—' else None
    key = pyDes.des(config.DES_KEY, pyDes.CBC, config.DES_IV)
    return map(extract,
        [key.decrypt(b64decode(service("PM25", scode))).decode("UTF-8")
            for scode in config.STATION.iterkeys()]
        )  # I'm too lazy...


def make_status(result):
    time = datetime.today().strftime(u"%d日%H时".encode("UTF-8")).decode('UTF-8')
    info = list()
    for i in result:
        if i[1] is not None:
            info.append(u"%s：%dμg/m³，国标AQI：%d(%s) 美标：%d(%s)"
                 % (i[0], i[1], i[2][0], i[2][1], i[3][0], i[3][1]))  # TODO it's ugly...
        else:
            info.append(u"%s: 暂无数据" % i[0])
    status = u"【%sPM2.5播报】%s" % (time, u'；'.join(info))
    if len(status) > 140:  # rarely happens
        status.replace(u"：", "")
    return status


def update_status(status):
    try:
        update(status, config.TWITTER)
    except:
        pass

    try:
        update(status, config.SINA)
    except:
        pass


def main():
    stations = config.STATION
    pm25 = read_pm25()
    aqi_china = map(lambda a: AQIChina(a)(), pm25)
    aqi_us = map(lambda a: AQIUS(a)(), pm25)
    result = zip(stations.values(), pm25, aqi_china, aqi_us)
    update_status(make_status(result))
    #print make_status(result).encode("GBK", 'ignore')


if __name__ == '__main__':
    main()
