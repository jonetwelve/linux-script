#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
usage:
    main.py -n k123 -n d123 -d 2016-12-12 上海 郑州

    options:
    -n 车次
    -d 日期
"""

# 忽略警告
import warnings
import requests
import threading

warnings.filterwarnings("ignore")

start = 'GYF'
to = 'ZAF'
# 车次
no = ['G660', 'G2014']
# no = ['G1926', 'G1930', 'G1954', 'G1938']
d = ['2017-01-25']

url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
    start, to)


def get_day_data(date):
    """
    获取当天的所有车次信息
    :param date:    查询日期
    :return:        车次信息list
    """
    real_url = url.format(date)
    response = requests.get(real_url, verify=False)

    return response.json().get('data')


def filter_no(item):
    """
    某个车次是否是要订票的车次
    :param item:
    :return:
    """
    if item.get('queryLeftNewDTO').get('station_train_code') in no:
        return True
    else:
        return False


def filter_empty(item):
    """
    判断某个车次是否有空座
    :param item:
    :return:
    """
    types = []
    types.append('yw_num')
    types.append('rw_num')
    types.append('zy_num')
    types.append('ze_num')

    for type in types:
        if item.get('queryLeftNewDTO').get(type) not in ['--', '无']:
            return True

    return False


def format_print(item):
    time = item.get('queryLeftNewDTO').get('start_train_date')
    date = time[4:6] + '-' + time[6:]
    code = item.get('queryLeftNewDTO').get('station_train_code')
    if item.get('queryLeftNewDTO').get('yw_num') not in ['--', '无']:
        type = '硬卧{}张'.format(item.get('queryLeftNewDTO').get('yw_num', 'ing'))
    if item.get('queryLeftNewDTO').get('rw_num') not in ['--', '无']:
        type = '软卧{}张'.format(item.get('queryLeftNewDTO').get('rw_num', 'ing'))
    if item.get('queryLeftNewDTO').get('zy_num') not in ['--', '无']:
        type = '一等座{}张'.format(item.get('queryLeftNewDTO').get('yw_num', 'ing'))
    if item.get('queryLeftNewDTO').get('ze_num') not in ['--', '无']:
        type = '二等座{}张'.format(item.get('queryLeftNewDTO').get('ze_num', 'ing'))

    return '{} {} {}'.format(date, code, type)


def show_table(date):
    back_data = get_day_data(date)
    for train in back_data:
        if filter_no(train) and filter_empty(train):
            print(format_print(train))

for date in d:
    threading.Thread(target=show_table, args=(date, )).start()
