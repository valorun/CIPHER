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
            "id": "1",
            "x": -210,
            "y": -183.984375,
            "label": "action:detail_de_laction",
            "shape": "box",
            "action": {
                "type": "action",
                "parametre_action1": "un param",
                "parametre_action2": 1
            }
        }
    ],
    [
        {
            "from": "start",
            "to": "1",
            "arrows": "to",
            "id": "f1"
        }
    ]
]
Il s'agit ici d'une séquence simple, où un seul noeud est relié au noeud de départ.