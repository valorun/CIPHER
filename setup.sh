#!/bin/bash

install_program(){
    while true; do
        read -p "Do you wish to install this program ? " yn
        case $yn in
            [Yy]* ) sudo apt-get install "$1"; break;;
            [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

### requirements ###
if type "python3" &>/dev/null; then
    echo "Python found"
else
    echo "Python3 not found"
    install_program "python3"
fi

if type "pip3" &>/dev/null; then
    echo "Pip found"
else
    echo "Pip not found"
    install_program "python3-pip"
fi

echo "Installing mplayer ..."
install_program "mplayer"
echo "Installing mosquitto ..."
install_program "mosquitto"
echo "Installing mosquitto-clients ..."
install_program "mosquitto-clients"

APP_PATH=$(cd $(dirname "$0") && pwd)

echo "Application path: $APP_PATH"

if [ -e $APP_PATH/requirements.txt ]
then
    echo "Installing python dependencies ..."
    pip3 install -r $APP_PATH/requirements.txt
else
    echo "No requirements file found."
fi


### add to startup ###
if [ -e /etc/rc.local ]
then
    if grep -q "nohup sudo $APP_PATH/app.py &" /etc/rc.local
    then
        echo "Program already added on startup."
    else
        while true; do
            read -p "Do you wish to add this program on startup ? " yn
            case $yn in
                [Yy]* ) sed -i -e "\$i \\nohup sudo $APP_PATH/app.py &\\n" /etc/rc.local; break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
else
    echo "No rc.local file found, can't add program on startup."
fi