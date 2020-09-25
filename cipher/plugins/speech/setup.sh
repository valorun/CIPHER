#!/usr/bin/env bash

### requirements ###
install_program "wget"
install_program "unzip"

PLUGIN_PATH=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
echo "Plugin path: $PLUGIN_PATH"

cd $PLUGIN_PATH
wget https://github.com/marytts/marytts/releases/download/v5.2/marytts-5.2.zip -O marytts.zip
unzip ./marytts.zip
rm marytts.zip
mv marytts-5.2 marytts
cd marytts

PLUGIN_PATH=$(cd $(dirname "$0") && pwd)

echo "Installing marytts ..."
$PLUGIN_PATH/bin/marytts-component-installer

### add to startup ###
add_to_startup "$PLUGIN_PATH/bin/marytts-server"