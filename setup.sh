#!/usr/bin/env bash

install_program(){
    if dpkg -s "$1" &>/dev/null; then
        echo "$1 found"
    else
        echo "\"$1\" not found"
        while true; do
            dialog --title "C.I.P.H.E.R" --clear --yesno "Do you wish to install \"$1\" ?" 5 50
            case $? in
                0) echo "Installing package \"$1\" ..."; sudo apt-get install "$1"; break;;
                1) clear; exit;;
                *) echo "Please answer yes or no.";;
            esac
        done
    fi
}

add_to_startup(){
    echo "Adding $1 to startup ..."
    if [ -e /etc/rc.local ]
    then
        if grep -q "nohup sudo $1 &" /etc/rc.local
        then
            echo "Program already added on startup."
        else
            while true; do
                dialog --title "C.I.P.H.E.R" --clear --yesno "Do you wish to add this program on startup ?" 5 50
                case $? in
                    0) sed -i -e "\$i \\nohup sudo $1 &\\n" /etc/rc.local; break;;
                    1) exit;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
        fi
    else
        echo "No rc.local file found, can't add program on startup."
    fi
}

if type "dialog" &>/dev/null; then
    echo "Dialog found"
else
    echo "Dialog not found"
    sudo apt-get install dialog
fi

### requirements ###
install_program "python3"
install_program "python3-pip"
install_program "mosquitto"
install_program "mosquitto-clients"

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
    fi
done
