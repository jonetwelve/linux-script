#!usr/bin/python3
# -*- coding:utf-8 -*-

"""redis 手册采集
http://doc.redisfans.com 内容采集
"""

import sqlite3
import requests, os, time
import re
from lxml import etree


header = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.88 Safari/537.36 Vivaldi/1.7.735.46',
	
}

re_content = re.compile('<div class="body">([\s\S]*)?          </div>\n        </div>\n      </div>\n      <div class="clearer"></div>')
re_cate = re.compile('<li><a href="index.html" accesskey="U">([^<]*?)</a> &raquo;</li>')
re_title = re.compile('<p><strong>([^<]*?)</strong></p>')

conn = sqlite3.connect('redis.sqlite3')
cursor = conn.cursor()
# conn.execute("INSERT INTO `document` (`category`,`content`) VALUES ()");

redis_url = 'http://doc.redisfans.com/'
url_html = requests.get(redis_url, headers=header)
selector = etree.HTML(url_html.text)
lis = selector.xpath('//li[@class="toctree-l2"]/a/@href')

for li in lis:
	content_url = redis_url + li
	try:
		content_html = requests.get(content_url, headers=header)
		cate = re_cate.findall(content_html.content.decode('utf-8'))[0].strip()
		content = re_content.findall(content_html.content.decode('utf-8'))[0].strip()
		title = re_title.findall(content_html.content.decode('utf-8'))[0].strip()
	
		cursor.execute("INSERT INTO `document` (`category`,`content`,`title`) VALUES ('%s','%s','%s')" % (cate, content, title))

		conn.commit()
	except:
		print(content_url)

	"""
	http://doc.redisfans.com/list/linsert.html
http://doc.redisfans.com/list/llen.html
http://doc.redisfans.com/list/lset.html
http://doc.redisfans.com/set/sdiff.html
http://doc.redisfans.com/set/sdiffstore.html
http://doc.redisfans.com/set/sismember.html
http://doc.redisfans.com/script/eval.html
http://doc.redisfans.com/script/evalsha.html
http://doc.redisfans.com/script/script_exists.html
http://doc.redisfans.com/script/script_load.html
http://doc.redisfans.com/server/bgsave.html
http://doc.redisfans.com/server/slaveof.html
http://doc.redisfans.com/server/sync.html
"""