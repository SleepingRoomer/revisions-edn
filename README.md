# Révisions EDN

Plateforme personnelle de révision pour les EDN : fiches par item, QCM au format EDN programmés à J1, J7 et J30, carnet d'erreurs, suivi par objectif LiSA, avancement par collège, planning.

**Site : https://sleepingroomer.github.io/revisions-edn/**

## Comment c'est construit

- **Ce dépôt (public)** contient uniquement le code du site : une seule page, `index.html`, sans dépendance ni serveur. Il ne contient aucune donnée.
- **Les données de chaque étudiant** vivent dans *son propre* dépôt GitHub, privé : QCM, résultats, carnet, relectures. Le format est décrit dans [`docs/FORMAT.md`](docs/FORMAT.md).
- Le site lit et écrit ce dépôt directement depuis le navigateur, avec une clé d'accès GitHub limitée à ce seul dépôt. La clé reste dans le navigateur de l'appareil.
- Les fiches et les QCM rédigés sont des Google Docs ; le site n'en garde que les liens.

Le site ne dépend donc ni de Claude ni d'aucun service autre que GitHub. Seule la **production du contenu** (fiches et séries de QCM) se fait avec un assistant : voir [`docs/GENERER-LES-QCM.md`](docs/GENERER-LES-QCM.md).

## Utiliser le site pour soi (autre étudiant)

1. Crée un dépôt **privé** sur GitHub, par exemple `revisions-edn-data`, avec un README.
2. Crée une clé d'accès : photo de profil › Settings › Developer settings › Personal access tokens › **Fine-grained tokens** › Generate new token.
   - Repository access : *Only select repositories* › ton dépôt de données.
   - Permissions › Repository permissions › **Contents : Read and write** (GitHub propose « Read-only » par défaut : change-le, sinon rien ne s'enregistre).
3. Ouvre le site, indique ton compte, le nom du dépôt et la clé. C'est tout : le site est vide jusqu'à ta première fiche.

Tu peux aussi *forker* ce dépôt pour modifier le site et le publier sur ton propre GitHub Pages (Settings › Pages › Deploy from a branch › `main` / root).

## Droits d'auteur

Les fiches LiSA, les collèges et les cours du CNPU sont protégés. Ne les publie pas dans un dépôt public : garde-les dans ton Drive et ton dépôt de données privé. Les QCM originaux que tu rédiges (ou fais rédiger) t'appartiennent.
