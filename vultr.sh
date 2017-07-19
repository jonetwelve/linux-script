#!/bin/bash

# get config
read -p "Input root passwd:" -s rootpwd
echo
read -p "Input shadowsocks passwd:" -s shadowsockspwd
# set password
(echo $rootpwd;sleep 1;echo $rootpwd) | passwd > /dev/null


######################centos
#关闭防火墙：
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
iptables -I INPUT -p tcp --dport 443 -j ACCEPT
service iptables save
#关闭selinux：
setenforce 0
#vim /etc/selinux/config
#SELINUX=enforcing改为SELINUX=disabled
######################centos end
 


yum update
yum install -y gcc python3-devel python-virtualenv python34-setuptools

# supervisor
yum install -y supervisor


# shadowsocks
easy_install-3.4 pip
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
echo '' >> /etc/supervisord.conf
echo '' >> /etc/supervisord.conf
echo '[program:ssserver]' >> /etc/supervisord.conf
echo 'command=ssserver -c /etc/shadowsocks.json' >> /etc/supervisord.conf
echo 'dirctory=/usr/local/bin' >> /etc/supervisord.conf
echo 'user=root' >> /etc/supervisord.conf
echo '' >> /etc/supervisord.conf


supervisord -c /etc/supervisord.conf
supervisotctl reload


yum install -y nginx 
pip3 install gunicorn
yum install -y mysql-server mysql mysql-devel


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
