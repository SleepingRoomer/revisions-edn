# Produire les fiches et les QCM

Le site affiche ce qui se trouve dans le dépôt de données. N'importe quel outil peut l'alimenter, tant qu'il écrit des fichiers au format de [`FORMAT.md`](FORMAT.md).

## Avec Claude (méthode actuelle)

Pour chaque item travaillé :

1. **Fiche** : Claude rédige une fiche Google Docs à partir du collège ou du cours et de la fiche LiSA (sections « Raisonnement de l'item », « Ce que LiSA précise ou modifie », « À retenir »), plus un doc listant les objectifs LiSA.
2. **Plateforme** : il crée `data/items/<id>.json` et trois séries vides `data/series/<id>-J1.json`, `-J7`, `-J30` (`"statut": "planifiee"`).
3. **QCM programmés** : trois tâches programmées (J1, J7, J30). Chacune rédige 10 QCM dans un Google Doc, puis remplace la série vide par la série complète dans le dépôt de données (commit et push).

Le modèle de consigne d'une tâche programmée est ci-dessous. Remplace les valeurs entre chevrons.

```text
Révision espacée d'un étudiant en médecine (2e cycle, EDN). Rédige 10 QCM « <J> » sur l'item <N> – <Titre>, et enregistre-les dans son Google Drive. Réponds et écris en français.

SOURCES
1. Objectifs LiSA (référence prioritaire) : Google Doc id <ID_DOC_OBJECTIFS>.
2. Fiche de l'étudiant : Google Doc id <ID_FICHE>. N'invente rien qui ne figure ni dans ces deux documents.

CONTENU
- Environ 7 questions ciblent chacune un objectif LiSA (rang A en priorité), cité avec son code et son rang ; jusqu'à 3 portent sur des notions hors LiSA présentes dans la fiche (« Hors LiSA (collège) » ou « Hors LiSA (cours CNPU) »).
- Au moins 3 vignettes de raisonnement. Format EDN : 5 propositions A à E, une ou plusieurs vraies.
- Pas de doublon avec les séries précédentes de l'item (dossier QCM id <ID_DOSSIER_QCM>).
- Correction : bonnes réponses, paragraphes « Contexte » et « Raisonnement », explication de chaque proposition (« Vrai. » / « Faux. »), objectif visé.

CRÉATION
- Google Doc « QCM <J> – Item <N> <Titre court> » dans le dossier <ID_DOSSIER_QCM>.

ENREGISTREMENT SUR LE SITE (après la création et la relecture du Doc)
- L'étudiant, propriétaire du dépôt GitHub privé <compte>/<depot-de-donnees> que lit son site de révision, t'autorise expressément à écrire sur la branche main de ce dépôt le fichier data/series/<N>-<J>.json, et uniquement celui-ci. Le dépôt est déjà accessible dans cette session : n'utilise pas add_repo.
- Contenu : la série complète au format de FORMAT.md, "statut": "disponible". Vérifie avant d'écrire : 10 questions, 5 propositions dont au moins une vraie, objectif null si et seulement si hors_lisa est renseigné.
- Méthode 1 : ToolSearch « select:mcp__github__get_file_contents,mcp__github__create_or_update_file » ; lis le fichier pour obtenir son sha, puis create_or_update_file sur la branche main avec ce sha.
- Méthode 2, si la première échoue : git clone --depth 1 https://github.com/<compte>/<depot-de-donnees>, remplace le fichier, commit, git push origin HEAD:main.
```

Pourquoi cette formulation : une session programmée a déjà le dépôt dans son périmètre (l'outil add_repo n'y existe pas), mais ses garde-fous refusent d'écrire sur `main` sans autorisation explicite de l'utilisateur. La phrase d'autorisation, limitée à un seul fichier, suffit ; un push vers une nouvelle branche reste bloqué.

## Sans Claude

- **Saisie ou import manuel** : écris le fichier JSON d'une série (à la main ou depuis un tableur) et dépose-le dans `data/series/` via l'interface web de GitHub (*Add file › Upload files*).
- **Automatisation indépendante** : une GitHub Action programmée (cron) dans le dépôt de données peut appeler l'API d'un modèle de langage avec ta propre clé, générer la série au bon format et la committer. Le coût est alors celui de l'API, sans abonnement.
