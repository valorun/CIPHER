#!/usr/bin/env bash

add_to_startup(){
    filename="$(basename $1)"
    echo "Adding $filename to startup ..."

    if [ -e "/etc/systemd/system/$filename" ]
    then
        echo "Program already added on startup."
    else
        while true; do
            read -p "Do you want to add this program on startup ? " yn
            case $yn in
                [Yy]* ) cp $1 /etc/systemd/system/
                        systemctl daemon-reload
                        systemctl enable $filename
                        systemctl start $filename
                        break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
}

### requirements ###
apt-get -y install "python3"
apt-get -y install "python3-pip"
apt-get -y install "mosquitto"
apt-get -y install "mplayer"

APP_PATH=$(cd $(dirname "$0") && pwd)
echo "Application path: $APP_PATH"
cd $APP_PATH/venv/bin/activate
python3 -m venv venv
source $APP_PATH

if [ -e $APP_PATH/requirements.txt ]
then
    echo "Installing python dependencies ..."
    pip3 install -U -r $APP_PATH/requirements.txt
else
    echo "No requirements file found."
fi


### add to startup ###
cat > $APP_PATH/cipher.service <<EOF
[Unit]
Description=CIPHER robotic server
After=network.target

[Service]
WorkingDirectory=$APP_PATH
ExecStart=$APP_PATH/venv/bin/python3 $APP_PATH/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

add_to_startup "$APP_PATH/cipher.service"

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