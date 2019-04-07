# Création d'une séquence

## Création pas à pas
Une séquence d'actions est créée de manière graphique dans l'onglet "Gestion des séquences".
Une fenêtre représentant un graph vide permet à l'utilisateur d'ajouter différents noeuds correspondant à des actions pouvant être ordonnées. Plusieurs actions sont à l'heure actuelle disponibles:
- Activer d'un relai
- Déplacer le robot
- Activer d'un servomoteur
- Jouer un son
- Prononcer une phrase
- Mettre la branche courante en pause

Les relais et servomoteurs pouvant être activés sont à définir préalablement dans l'onglet "Paramètres".
Une séquence peut contenir plusieurs actions en parallèle. Par exemple, si plusieurs actions sont reliées à un noeud même noeud, celles-ci seront toutes executées en même temps après l'action du noeud courant.

## Aspect technique

La création s'effectue à l'aide de la bibliothèque vis.js, destinée au tracé de graph.
Le format de stockage utilisé est JSON, utilisé par la bibliothèque.
Une séquence se présente sous la forme suivante:
[
    [
        {
            "id": "start",
            "label": "Start",
            "color": "red"
        },
        {
            "id": "004d1725-568a-4c2e-9989-99b0869f1adb",
            "x": -210,
            "y": -183.984375,
            "label": "relay:test,1",
            "shape": "box",
            "action": {
                "type": "action",
                "parametre_action1": "un param",
                "parametre_action2": 1
            }
        },
        {
            "id": "03568e98-6c07-446b-b35a-75bc20548792",
            "x": -204,
            "y": -153.984375,
            "label": "speech:'fff'",
            "shape": "box",
            "action": {
                "type": "speech",
                "speech": "fff"
            }
        },
        {
            "id": "4a0adb37-19a2-49cb-92f2-5f0be3086371",
            "x": -141,
            "y": -105.984375,
            "label": "script:test.py",
            "shape": "box",
            "action": {
                "script": "test.py",
                "type": "script"
            }
        },
        {
            "id": "a47e8f52-cbd9-4461-8fe8-c99a934bf1a0",
            "x": -205,
            "y": -148.984375,
            "label": "sound:son_test.mp3",
            "shape": "box",
            "action": {
                "sound": "son_test.mp3",
                "type": "sound"
            }
        },
        {
            "id": "0fee7266-8a46-47d8-adfb-423c4df75cba",
            "x": -233,
            "y": -138.984375,
            "label": "pause:100ms",
            "shape": "circle",
            "action": {
                "type": "pause",
                "time": 100
            }
        }
    ],
    [
        {
            "from": "start",
            "to": "004d1725-568a-4c2e-9989-99b0869f1adb",
            "arrows": "to",
            "id": "6cba42b2-40a6-4feb-8f21-c83373a22d94"
        },
        {
            "from": "start",
            "to": "03568e98-6c07-446b-b35a-75bc20548792",
            "arrows": "to",
            "id": "e765ee97-cbaa-4a74-8781-4b9ee492705e"
        },
        {
            "from": "03568e98-6c07-446b-b35a-75bc20548792",
            "to": "4a0adb37-19a2-49cb-92f2-5f0be3086371",
            "arrows": "to",
            "id": "67bc6982-03d4-4f54-97ab-aef9b6a6b9d1"
        },
        {
            "from": "4a0adb37-19a2-49cb-92f2-5f0be3086371",
            "to": "a47e8f52-cbd9-4461-8fe8-c99a934bf1a0",
            "arrows": "to",
            "id": "e282ecfd-ae5f-41c0-9f6d-c9e71f076639"
        },
        {
            "from": "a47e8f52-cbd9-4461-8fe8-c99a934bf1a0",
            "to": "0fee7266-8a46-47d8-adfb-423c4df75cba",
            "arrows": "to",
            "id": "929a1e29-e8d6-4cee-9b0d-9d3128c91371"
        }
    ]
]