# Révisions EDN

Plateforme gratuite de révision pour les EDN : fiches par item, séries au format des épreuves dématérialisées (QRU, QRM, QRP, QROC, TCS, zones à pointer, dossiers progressifs, KFP) programmées à J1, J7 et J30, notation du CNG et note validante de rang A, carnet d'erreurs, suivi par objectif de connaissance.

**Site : https://sleepingroomer.github.io/revisions-edn/**
**Guide pour les étudiants : https://sleepingroomer.github.io/revisions-edn/#guide**

## Pour un étudiant

Rien à installer, compte facultatif : on ouvre le lien et on clique sur « Commencer ». Le guide intégré au site explique tout, pas à pas.

- **Fiches** : on choisit un item (1 à 367) ; son titre et ses objectifs de connaissance officiels se remplissent depuis le programme (`programme.json`, tiré de l'arrêté du 24 juillet 2023). On y relie sa propre fiche (Google Docs, Notion, PDF…).
- **Fiches de la plateforme** : des fiches rédigées pour le site (`fiches/index.json` et `fiches/<item>.json`) apparaissent dans l'onglet Fiches et sa recherche, et se lisent sans rien importer.
- **Iconographies** : sur chaque fiche, les images attendues par le programme (objectifs « contenu multimédia ») sont listées ; l'étudiant y ajoute ses images (lien ou fichier), se teste dessus, et les questions des séries peuvent s'appuyer dessus.
- **Séries de QCM** : le site rédige une consigne complète que l'étudiant colle dans l'IA de son choix (ChatGPT, Le Chat, Gemini, Claude…) avec sa fiche ; il colle la réponse dans le site, qui la vérifie et l'enregistre. Le format texte attendu est décrit dans [`docs/FORMAT.md`](docs/FORMAT.md).
- **Données** : elles restent dans le navigateur de l'étudiant (IndexedDB). Personne d'autre n'y a accès. Une sauvegarde dans un fichier permet de les garder et de changer d'appareil.
- **Compte (facultatif)** : avec une adresse mail et un pseudo, sans mot de passe. Il garde une copie de la progression dans la banque de questions, des réglages et des questions de la banque rangées dans le carnet, et permet de signaler une erreur dans une question ou de confirmer qu'elle est juste. Les fiches et les séries personnelles n'y vont pas.

## Option avancée : données dans un dépôt GitHub

Pour synchroniser plusieurs appareils automatiquement, ou faire rédiger les séries par des tâches programmées :

1. Crée un dépôt **privé** sur GitHub, par exemple `revisions-edn-data`, avec un README.
2. Crée une clé d'accès : photo de profil › Settings › Developer settings › Personal access tokens › **Fine-grained tokens** › Generate new token.
   - Repository access : *Only select repositories* › ton dépôt de données.
   - Permissions › Repository permissions › **Contents : Read and write** (GitHub propose « Read-only » par défaut : change-le, sinon rien ne s'enregistre).
3. Sur l'écran d'accueil du site, ouvre « Option avancée », indique ton compte, le nom du dépôt et la clé. Elle reste dans le navigateur de l'appareil.

Les tâches programmées décrites dans [`docs/GENERER-LES-QCM.md`](docs/GENERER-LES-QCM.md) écrivent alors les séries directement dans ce dépôt.

## Comment c'est construit

- **Ce dépôt (public)** contient le code du site, une seule page `index.html` sans dépendance ni serveur, et `programme.json` (texte public du programme officiel). Il ne contient aucune donnée personnelle.
- Le site lit et écrit soit dans le navigateur, soit dans un dépôt GitHub privé, avec le même format de documents.
- Les comptes, les signalements et la copie de la progression passent par une base Supabase, appelée directement depuis la page (bloc « Compte » de `index.html`). Sans réseau ou sans compte, le site fonctionne comme avant. `outils/test_compte.py` rejoue le parcours du compte dans un navigateur contre une fausse base.

Tu peux *forker* ce dépôt pour modifier le site et le publier sur ton propre GitHub Pages (Settings › Pages › Deploy from a branch › `main` / root).
