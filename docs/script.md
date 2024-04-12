# Création d'un script

Les scripts sont des morceaux de codes pouvant être executés dans des séquences.
Ils peuvent manipuler différentes données qui leurs sont passés en paramètre via la variable 'kwargs'.

## Emplacement

Afin de pouvoir il être executés, les scripts doivent se trouver dans le dossier prévu à cet effet dans ```cipher/scripts```

## Structure

La seconde condition à l'execution d'un script est sa validité. `
En effet, pour pouvoir être appelé, il doit contenir au minimun une fonction 'main' avec la signature suivante: ```def main(**kwargs):```.

