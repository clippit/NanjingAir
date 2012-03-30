#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
from suds.client import Client
import config
from aqi import aqi_pm25, aqi_desc


def read_pm25():
    client = Client(config.WSDL)
    extract = lambda s: int(s[8: s.find(u'微克')]) if s[9] != u'—' else None
    return map(extract,
        [unicode(client.service.getSurvyValue("PM25", scode))
            for scode in config.STATION.iterkeys()]
        )  # I'm too lazy...


def make_status(result):
    time = datetime.today().strftime(u"%m月%d日%H时".encode("UTF-8")).decode('UTF-8')
    info = list()
    for i in result:
        if i[1] is not None:
            info.append(u"%s: %d, 参考AQI: %d(%s)" % i)
        else:
            info.append(u"%s: 暂无数据" % i[0])
    return u"【%s PM2.5浓度播报】%s" % (time, u'；'.join(info))


def main():
    stations = config.STATION
    pm25 = read_pm25()
    aqi = map(aqi_pm25, pm25)
    desc = map(aqi_desc, aqi)
    result = zip(stations.values(), pm25, aqi, desc)
    print (make_status(result))


if __name__ == '__main__':
    main()
