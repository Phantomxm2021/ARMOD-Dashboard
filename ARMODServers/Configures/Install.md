# init server
```
apt-get update
apt-get upgrade
```

# Install Ngnix
apt-get install Ngnix

# Install git
apt-get install git

pip3 install virutalenv


# Error
```
/bin/sh: 1: mysql_config: not found
...
ERROR: Could not find a version that satisfies the requirement mysqlclient==2.0.3
ERROR: No matching distribution found for mysqlclient==2.0.3
```
centos系统使用yum安装 mysql-devel

yum install mysql-devel

ubuntu 系统apt-get 安装libmysqlclient-dev

apt-get update
apt-get upgrade
apt-get install libmysqlclient-dev

debian 系统

apt install -y libmariadbd18
apt install -y libmariadbd-dev


apt-get install redis-server