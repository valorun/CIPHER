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

APP_PATH=$(cd $(dirname "$0") && pwd)

echo "Application path: $APP_PATH"

if [ -e $APP_PATH/requirements.txt ]
then
    echo "Installing python dependencies ..."
    pip3 install -r $APP_PATH/requirements.txt
else
    echo "No requirements file found."
fi

### SSL certificate ###
if type "openssl" &>/dev/null; then
    echo "OpenSSL found"
else
    echo "OpenSSL not found"
    install_program "openssl"
fi

generate_certificate(){
    echo "Generating self-signed SSL certificate ..."
    openssl req -x509 -newkey rsa:4096 -keyout $APP_PATH/key.pem -out $APP_PATH/cert.pem -days 365 -nodes
}

if [ -e $APP_PATH/key.pem -o -e $APP_PATH/cert.pem ]
then
    echo "Some certificates already exists in the application directory."
    while true; do
        read -p "Do you wish to generate a new certificate ? " yn
        case $yn in
            [Yy]* ) generate_certificate; break;;
            [Nn]* ) break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
else
    generate_certificate
fi

### add to startup ###
if [ -e /etc/rc.local ]
then
    if grep -q "nohup $APP_PATH/app.py &" /etc/rc.local
    then
        echo "Program already added on startup."
    else
        while true; do
            read -p "Do you wish to add this program on startup ? " yn
            case $yn in
                [Yy]* ) sed -i -e "\$i \\nohup $APP_PATH/app.py &\\n" /etc/rc.local; break;;
                #[Yy]* ) sed -i -e "\$i \\sudo python3 $APP_PATH/app.py &\\n" ./test; break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
else
    echo "No rc.local file found, can't add program on startup."
fi