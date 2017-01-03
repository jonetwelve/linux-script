#!/usr/bin/python3
# -*- coding:utf-8 -*-

from prettytable import PrettyTable
import subprocess
import sys

try:
    lines = sys.argv[1]
except:
    lines = str(5)

command = 'git log -' + lines + ' --pretty=format:"%h %an %s"'

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
