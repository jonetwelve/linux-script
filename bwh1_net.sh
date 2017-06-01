#!/bin/bash

# get config
read -p "Input root passwd:" -s rootpwd
echo
read -p "Input shadowsocks passwd:" -s shadowsockspwd


# set password
(echo $rootpwd;sleep 1;echo $rootpwd) | passwd > /dev/null

apt update
apt install -y python3-pip gcc python3-dev python3-venv

# supervisor
apt install -y supervisor
#### auto start
systemctl start supervisor
systemctl enable supervisor


# shadowsocks
apt install -y python-gevent
pip3 install setuptools
pip3 install shadowsocks
#### write the config
echo '{' > /etc/shadowsocks.json
echo '"server":"0.0.0.0",' >> /etc/shadowsocks.json
echo '"server_port":443,' >> /etc/shadowsocks.json
echo '"local_port":1080,' >> /etc/shadowsocks.json
echo '"password":"${shadowsockspwd}",' >> /etc/shadowsocks.json
echo '"timeout":600,' >> /etc/shadowsocks.json
echo '"method":"aes-256-cfb"' >> /etc/shadowsocks.json
echo '}' >> /etc/shadowsocks.json
#### auto start
echo '[program:ssserver]' >> /etc/supervisor/conf.d/ssserver.conf
echo 'command=ssserver -c /etc/shadowsocks.json' >> /etc/supervisor/conf.d/ssserver.conf
echo 'dirctory=/usr/local/bin' >> /etc/supervisor/conf.d/ssserver.conf
echo 'user=root' >> /etc/supervisor/conf.d/ssserver.conf


apt install -y nginx gunicorn
apt install -y mariadb-server
apt install -y libmysqlclient-dev

:<<'
----ngin.conf
server {
        listen  80;
        server_name domain1 domain2;

        location / {
                proxy_pass http://127.0.0.1:5000;
                proxy_set_header Host $host;
        	    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}

----supervisor
[program:domain]
directory=/domain/path
command=gunicorn -w 4 -b 127.0.0.1 run:app
user=www-data
'
