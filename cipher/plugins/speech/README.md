# NeuTTS Speech Plugin

Ce plugin utilise [NeuTTS](https://github.com/neuphonic/neutts) pour offrir une synthèse vocale moderne et rapide. 
Il a été allégé pour ne plus dépendre de PyTorch en production, reposant uniquement sur `llama-cpp-python` et `onnxruntime`.

## Créer une nouvelle voix

La création de voix nécessite d'encoder un fichier audio via PyTorch. Pour ne pas alourdir l'application en production, cette étape doit être effectuée dans l'environnement de développement `dev` (qui contient `torch` et la librairie complète `neucodec`).

1. Placez-vous à la racine du projet CIPHER.
2. Utilisez le script `create_voice.py` en lançant la commande suivante :

```bash
pixi run -e dev python cipher/plugins/speech/create_voice.py \
    --wav "chemin/vers/mon_audio.wav" \
    --text "Le texte exact prononcé dans cet audio, avec ponctuation." \
    --name "ma_nouvelle_voix"
```

Le script générera deux fichiers dans le dossier `cipher/plugins/speech/voices/` :
- `ma_nouvelle_voix.npy` (l'empreinte vocale encodée)
- `ma_nouvelle_voix.txt` (le texte de référence)

La nouvelle voix apparaîtra automatiquement dans le menu déroulant de l'interface web au prochain chargement de la page.
