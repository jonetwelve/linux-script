#!/usr/bin/python3
# -*- coding:utf-8 -*-

from prettytable import PrettyTable
import subprocess
import datetime
import sys

try:
    ago = int(sys.argv[1])
except:
    ago = 5

four_days_before = (datetime.datetime.now() - datetime.timedelta(days=ago)).strftime('%Y-%m-%d')
command = 'git log --pretty=format:"%h %an %s" --since={' + four_days_before + '}'

gitlog = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True).communicate()

pt = PrettyTable(['Hash', 'Author', 'Commit'])
pt.align['Commit'] = "l"


def print_color():
    i = 31
    while True:
        yield i
        i += 1
        if i > 37:
            i = 31


color = print_color()

for line in gitlog[0].decode().split('\n'):
    item = line.split(maxsplit=2)
    item[0] = '\033[%dm' % (color.__next__(),) + item[0]
    pt.add_row(item)

print(pt)
