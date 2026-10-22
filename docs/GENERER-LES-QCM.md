# Produire les fiches et les QCM

Le site affiche ce qui se trouve dans le dépôt de données. N'importe quel outil peut l'alimenter, tant qu'il écrit des fichiers au format de [`FORMAT.md`](FORMAT.md).

## Avec Claude (méthode actuelle)

Les consignes de rédaction sont dans le dépôt de données lui-même, pour qu'une seule source fasse foi :

- `outils/CONSIGNES-QCM.md` : composition d'une série (7 questions isolées et un bloc DP, KFP ou TCS), manière d'écrire des épreuves nationales, règles par format, correction, Google Doc et JSON au format 2 ;
- `outils/verifier_serie.py` : contrôle d'une série avant enregistrement ;
- `outils/planifier.py` : planification adaptative après J30 (intervalle selon la note et le rang A, plafond de 120 jours, phase finale avant les EDN) ;
- `outils/programme-officiel.json` : objectifs de connaissance de l'arrêté du 24 juillet 2023, par item ;
- `data/items/<id>.json` : `titre_doc` et `notes_qcm`, consignes propres à l'item.

Pour chaque fiche : trois tâches programmées (J1, J7, J30) rédigent chacune une série selon ces consignes. Une tâche quotidienne lance `planifier.py`, crée les séries suivantes et rédige celles du jour.

Modèle de consigne d'une tâche J1, J7 ou J30 :

```text
Révision espacée d'un étudiant en médecine (EDN). Rédige la série « <J> » de l'item <id> et enregistre-la. Réponds et écris en français.

1. git clone --depth 1 https://github.com/<compte>/<depot-de-donnees> /tmp/rev
2. Lis /tmp/rev/outils/CONSIGNES-QCM.md, rédigé à ma demande : suis-le entièrement.
3. Paramètres : item <id> (data/items/<id>.json), série <J>, date <AAAA-MM-JJ>.
4. Je t'autorise expressément à écrire sur la branche main de ce dépôt le fichier data/series/<id>-<J>.json, et uniquement celui-ci. Le dépôt est déjà accessible dans cette session : n'utilise pas add_repo.
```

## Sans Claude

- **Saisie ou import manuel** : écris le fichier JSON d'une série (à la main ou depuis un tableur) et dépose-le dans `data/series/` via l'interface web de GitHub (*Add file › Upload files*).
- **Automatisation indépendante** : une GitHub Action programmée (cron) dans le dépôt de données peut appeler l'API d'un modèle de langage avec ta propre clé, générer la série au bon format et la committer. Le coût est alors celui de l'API, sans abonnement.
