# **C.I.P.H.E.R**
![alt text](https://raw.githubusercontent.com/valorun/CIPHER/dev/app/static/img/capture.png)
Interface de contrôle du projet de robotique C.I.P.H.E.R. Il s'agit d'une interface web réalisée en HTML/Js permettant une connexion à un raspberry via un serveur Python Flask. En outre, l'utilisateur peut ordonner l'exécution de commandes sur les raspberries inter-connectés, tel que l'activation de relais ou de servo-moteurs.
# Pré-requis
- Python3 sur le raspberry serveur
- Navigateur Google Chrome côté client (La Web Speech API est pour l'instant uniquement disponible sur celui-ci)
# Installation
Téléchargez et décompressez l'archive de C.I.P.H.E.R sur le serveur à l'emplacement désiré.
Dans le cadre de notre exemple, il s'agira de ```/home/pi```.
Pour mettre en route le serveur au démarage du raspberry, plusieurs méthodes existent.
Dans notre cas, la ligne ```sudo python /home/pi/CIPHER/app.py``` est ajoutée avant le 'exit 0' du fichier ```etc/rc.local```.
Le serveur peut ensuite être accédé depuis l'adresse du raspberry dans un navigateur avec le port 5000. dans notre cas, il s'agit de l'adresse suivante :```https://192.168.1.78:5000```.

# Bibliothèques utilisées
## Python
- flask (http://flask.pocoo.org/)
- flask-socketio (https://flask-socketio.readthedocs.io/en/latest/)
- ChatterBot (https://github.com/gunthercox/ChatterBot)
- flask_sqlalchemy (http://flask-sqlalchemy.pocoo.org/2.3/)

## JavaScript
- jQuery (https://jquery.com/)
- js-cookie (https://github.com/js-cookie/js-cookie)
- gridstack.js (https://github.com/gridstack/gridstack.js)
- lodash (https://lodash.com/)
- socket.io (https://github.com/socketio/socket.io)
- JsSpeechRecognizer (https://github.com/dreamdom/JsSpeechRecognizer)
- vis.js (https://github.com/almende/vis/tree/develop)
