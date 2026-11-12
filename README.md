# Révisions EDN

Plateforme gratuite de révision pour les EDN : fiches par item, séries au format des épreuves dématérialisées (QRU, QRM, QRP, QROC, TCS, dossiers progressifs, KFP) programmées à J1, J7 et J30, notation du CNG et note validante de rang A, carnet d'erreurs, suivi par objectif de connaissance.

**Site : https://sleepingroomer.github.io/revisions-edn/**
**Guide pour les étudiants : https://sleepingroomer.github.io/revisions-edn/#guide**

## Pour un étudiant

Rien à installer, pas de compte : on ouvre le lien et on clique sur « Commencer ». Le guide intégré au site explique tout, pas à pas.

- **Fiches** : on choisit un item (1 à 367) ; son titre et ses objectifs de connaissance officiels se remplissent depuis le programme (`programme.json`, tiré de l'arrêté du 24 juillet 2023). On y relie sa propre fiche (Google Docs, Notion, PDF…).
- **Iconographies** : sur chaque fiche, les images attendues par le programme (objectifs « contenu multimédia ») sont listées ; l'étudiant y ajoute ses images (lien ou fichier), se teste dessus, et les questions des séries peuvent s'appuyer dessus.
- **Séries de QCM** : le site rédige une consigne complète que l'étudiant colle dans l'IA de son choix (ChatGPT, Le Chat, Gemini, Claude…) avec sa fiche ; il colle la réponse dans le site, qui la vérifie et l'enregistre. Le format texte attendu est décrit dans [`docs/FORMAT.md`](docs/FORMAT.md).
- **Données** : elles restent dans le navigateur de l'étudiant (IndexedDB). Personne d'autre n'y a accès. Une sauvegarde dans un fichier permet de les garder et de changer d'appareil.

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

Tu peux *forker* ce dépôt pour modifier le site et le publier sur ton propre GitHub Pages (Settings › Pages › Deploy from a branch › `main` / root).

## Droits d'auteur

Les fiches d'objectifs, les collèges et les cours du CNPU sont protégés, images comprises : le site n'en fournit pas et n'en publie pas. Les iconographies qu'un étudiant ajoute restent dans ses données personnelles (son navigateur ou son dépôt privé). Chaque étudiant relie ses propres fiches. Les QCM que tu rédiges (ou fais rédiger) t'appartiennent.
