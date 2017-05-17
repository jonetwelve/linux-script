#!/bin/bash

# get config
read -p "Input root passwd:" -s rootpwd
echo
read -p "Input shadowsocks passwd:" -s shadowsockspwd


# set password
(echo $rootpwd;sleep 1;echo $rootpwd) | passwd > /dev/null

apt update
apt install -y pythoni3-pip gcc python3-dev

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


apt install -y nginx
apt install -y mariadb-server
apt install -y libmysqlclient-dev

