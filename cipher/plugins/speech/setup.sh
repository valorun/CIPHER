#!/usr/bin/env bash

### requirements ###
apt-get -y install "wget"
apt-get -y install "unzip"
apt-get -y install "default-jre"

PLUGIN_PATH=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
echo "Plugin path: $PLUGIN_PATH"

cd $PLUGIN_PATH
wget https://github.com/marytts/marytts/releases/download/v5.2/marytts-5.2.zip -O marytts.zip
unzip ./marytts.zip
rm marytts.zip
mv marytts-5.2 marytts
cd marytts
wget https://github.com/marytts/voice-upmc-pierre-hsmm/releases/download/v5.2/voice-upmc-pierre-hsmm-5.2.zip -O voice-upmc-pierre-hsmm.zip
extract voice-upmc-pierre-hsmm.zip
mv voice-upmc-pierre-hsmm.zip ./download

PLUGIN_PATH=$(cd $(dirname "$0") && pwd)

echo "Installing marytts ..."
#$PLUGIN_PATH/bin/marytts-component-installer

### add to startup ###
add_to_startup "$PLUGIN_PATH/bin/marytts-server"