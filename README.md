# **Clarius**
Interface de controle du projet de robotique Hector. Il s'agit d'une interface web réalisée en HTML/Js permettant une connexion à un raspberry via un serveur Python Flask. En outre, l'utilisateur peut ordonner l'execution de commandes sur les raspberries inter-connectés, tel que l'activation de relais ou de servo-moteurs.

# Pré-requis
- Python3 sur le raspberry serveur
- Navaigateur Google Chrome côté client (La Web Speech API est pour l'instant uniquement disponible sur celui-ci)

# Installation
Téléchargez et décompressez l'archive d'Hector sur le serveur à l'emplacement désité.
Dans le cadre de notre exemple, il s'agira de ```/home/pi```.
Afin de permettre de se connecter au serveur, il convient d'abord de fournir l'adresse du serveur au client.
Pour cela, modifiez le fichier ```app/static/js/connection.js``` et changez l'adresse ```192.168.1.78:5000``` par l'adresse du respberry.
Pour executer le serveur au démarage du raspberry, plusieurs méthodes existent.
Dans notre cas, la ligne ```sudo python /home/pi/Hector/app.py``` est ajoutée avant le 'exit 0' du fichier ```etc/rc.local```.

Le serveur peut ensuite être accédé depuis l'adresse ```https://192.168.1.78:5000``` dans le navigateur.
