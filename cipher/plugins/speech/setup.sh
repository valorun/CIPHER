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
echo "Installing wget ..."
install_program "wget"
echo "Installing unzip ..."
install_program "unzip"

wget https://github.com/marytts/marytts/releases/download/v5.2/marytts-5.2.zip -O marytts.zip
unzip ./marytts.zip
mv marytts-5.2 marytts
cd marytts

APP_PATH=$(cd $(dirname "$0") && pwd)

echo "Application path: $APP_PATH"
echo "Installing marytts ..."
$APP_PATH/bin/marytts-component-installer

### add to startup ###
if [ -e /etc/rc.local ]
then
    if grep -q "nohup sudo $APP_PATH/bin/marytts-server &" /etc/rc.local
    then
        echo "Program already added on startup."
    else
        while true; do
            read -p "Do you wish to add this program on startup ? " yn
            case $yn in
                [Yy]* ) sed -i -e "\$i \\nohup sudo $APP_PATH/bin/marytts-server &\\n" /etc/rc.local; break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
else
    echo "No rc.local file found, can't add program on startup."
fi