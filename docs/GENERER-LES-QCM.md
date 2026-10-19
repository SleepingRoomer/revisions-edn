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

ENREGISTREMENT SUR LE SITE
- Attache le dépôt <compte>/<depot-de-donnees> avec l'outil add_repo (access « push ») et clone-le.
- Suis docs/ENREGISTRER.md du dépôt de données : remplace data/series/<N>-<J>.json par la série complète, valide le JSON, commit, push.
```

## Sans Claude

- **Saisie ou import manuel** : écris le fichier JSON d'une série (à la main ou depuis un tableur) et dépose-le dans `data/series/` via l'interface web de GitHub (*Add file › Upload files*).
- **Automatisation indépendante** : une GitHub Action programmée (cron) dans le dépôt de données peut appeler l'API d'un modèle de langage avec ta propre clé, générer la série au bon format et la committer. Le coût est alors celui de l'API, sans abonnement.
