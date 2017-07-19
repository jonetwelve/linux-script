#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
usage:
    once.py -n k123 -n d123 -d 2016-12-12 上海 郑州

    options:
    -n 车次
    -d 日期
"""

# 忽略警告
import warnings
import getopt
import sys
import cities
import requests
import threading
from prettytable import PrettyTable
import re

re_color = re.compile('_(.*?)_')

warnings.filterwarnings("ignore")

options, args = getopt.getopt(sys.argv[1:], "n:d:")

if len(args) < 2:
    print(__doc__)
    sys.exit()

# 车次
no = []
# 日期
date = []

for name, value in options:
    # 处理类型
    if name in ['-n']:
        no.append(value)
    elif name in ['-d']:
        date.append(value)

if len(date) < 1:
    print(__doc__)
    sys.exit()

# 出发地
from_station = args[0]
# 目的地
to_station = args[1]

headers = 'No Date Start Ing Stop Hard Soft Site1 Site2'.split()

url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
    cities.cities.get(from_station, ''), cities.cities.get(to_station, ''))


def get_day_data(date):
    """
    获取当天的所有车次信息
    :param date:    查询日期
    :return:        车次信息list
    """
    real_url = url.format(date)
    response = requests.get(real_url, verify=False)

    return response.json().get('data')


def filter_empty(item):
    """
    判断某个车次是否有空座
    :param item:
    :return:
    """
    types = []
    types.append('yw_num')
    types.append('rw_num')
    # types.append('gr_num')
    types.append('zy_num')
    types.append('ze_num')
    # types.append('swz_num')

    for type in types:
        if item.get('queryLeftNewDTO').get(type) not in ['--', '无']:
            return True

    return False


def color_warning(tmp):
    if tmp != 'null':
        tmp = '_' + tmp + '_'
    return tmp


def get_useful_data(item):
    if filter_no(item):
        date = item.get('queryLeftNewDTO').get('start_train_date')
        yw = color_warning(
            item.get('queryLeftNewDTO').get('yw_num').replace(
                '无', 'null').replace(
                '--', 'null'))
        zy = color_warning(
            item.get('queryLeftNewDTO').get('zy_num').replace(
                '无', 'null').replace(
                '--', 'null'))
        rw = color_warning(
            item.get('queryLeftNewDTO').get('rw_num').replace(
                '无', 'null').replace(
                '--', 'null'))
        ze = color_warning(
            item.get('queryLeftNewDTO').get('ze_num').replace(
                '无', 'null').replace(
                '--', 'null'))
        back = [
            item.get('queryLeftNewDTO').get('station_train_code'),
            date[4:6] + '-' + date[6:],
            item.get('queryLeftNewDTO').get('start_time'),
            item.get('queryLeftNewDTO').get('lishi'),
            item.get('queryLeftNewDTO').get('arrive_time'),
            yw,
            rw,
            zy,
            ze,
        ]
        return back
    else:
        return []


def filter_no(item):
    """
    某个车次是否是要订票的车次
    :param item:
    :return:
    """
    if len(no) > 0:
        if item.get('queryLeftNewDTO').get('station_train_code') in no:
            return True
        else:
            return False
    else:
        return True


def show_table(date):
    back_data = get_day_data(date)
    pt = PrettyTable()
    pt._set_field_names(headers)
    for item in back_data:
        td = get_useful_data(item)
        if len(td) > 0:
            pt.add_row(td)
    tmp = str(pt)
    print(re_color.sub(r'${color red} \1 ${color}', tmp))
    print('')


print(from_station, '~', to_station)
for d in date:
    threading.Thread(target=show_table, args=(d,)).start()
