#!/bin/bash

INI="uwsgi.ini"
UWSGI=" /home/virtualenv/armod_env/bin/uwsgi"
PSID="ps aux | grep "uwsgi"| grep -v "grep" | wc -l"

if [ ! -n "$1" ]
then
    content="Usages: sh uwsgiserver.sh [start|stop|restart]"
    echo -e "\033[31m $content \033[0m"
    exit 0
fi
 
if [ $1 = start ]
then
    if [ `eval $PSID` -gt 4 ]
    then
        content="uwsgi is running!"
        echo -e "\033[32m $content \033[0m"
        exit 0
    else
        $UWSGI $INI
        content="Start uwsgi service [OK]"
        echo -e "\033[32m $content \033[0m"
    fi
 
elif [ $1 = stop ];then
    if [ `eval $PSID` -gt 4 ];then
        killall -9 uwsgi
    fi
    content="Stop uwsgi service [OK]"
    echo -e "\033[32m $content \033[0m"
elif [ $1 = restart ];then
    if [ `eval $PSID` -gt 4 ];then
        killall -9 uwsgi
    fi
    $UWSGI --ini $INI
    content="Restart uwsgi service [OK]"
    echo -e "\033[32m $content \033[0m"

else
    content="Usages: sh uwsgiserver.sh [start|stop|restart]"
    echo -e "\033[31m $content \033[0m"
fi