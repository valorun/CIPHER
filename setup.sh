#!/usr/bin/env bash

add_to_startup(){
    if [ "$DOCKER" = true ]
    then
        return 0
    fi

    echo "Adding $1 to startup ..."
    if [ -e /etc/rc.local ]
    then
        if grep -q "nohup sudo $1 &" /etc/rc.local
        then
            echo "Program already added on startup."
        else
            while true; do
                read -p "Do you want to add this program on startup ? " yn
                case $yn in
                    [Yy]* ) sed -i -e "\$i \\nohup sudo $1 &\\n" /etc/rc.local; break;;
                    [Nn]* ) exit;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
        fi
    else
        echo "No rc.local file found, can't add program on startup."
    fi
}

DOCKER=false
if [ $# -ne 0 ]
then
	case "$1" in
	"docker") DOCKER=true;;
	esac
fi

### requirements ###
if [ "$DOCKER" = false ]
then
    apt-get -y install "python3"
    apt-get -y install "python3-pip"
fi

apt-get -y install "mosquitto"
apt-get -y install "mplayer"

APP_PATH=$(cd $(dirname "$0") && pwd)
echo "Application path: $APP_PATH"

if [ -e $APP_PATH/requirements.txt ]
then
    echo "Installing python dependencies ..."
    pip3 install -U -r $APP_PATH/requirements.txt
else
    echo "No requirements file found."
fi


### add to startup ###
add_to_startup "$APP_PATH/app.py"

for D in cipher/plugins/*; do
    if [ -d "${D}" ]; then
        if [ -f ${D}/setup.sh ]; then
            echo "Setting up plugin in ${D} ..."
            source "${D}/setup.sh"
            cd $APP_PATH
        fi
        if [ -f ${D}/requirements.txt ]; then
            echo "Installing python dependencies for plugin in ${D} ..."
            pip3 install -U -r ${D}/requirements.txt
        fi
    fi
done
