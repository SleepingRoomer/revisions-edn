# Banque commune de questions

La banque commune est un ensemble de fichiers du site, lisibles par tous sans compte :

```
banque/index.json      sommaire : nombre de questions par item et par objectif
banque/<item>.json     toutes les questions d'un item du programme (banque/193.json, banque/47.json)
```

Le site lit `index.json` au démarrage, puis ne charge que les fichiers des items dont il a besoin. La progression de l'étudiant n'est pas ici : elle reste sur son appareil (et dans Supabase s'il synchronise), et renvoie aux questions par leur identifiant.

## banque/&lt;item&gt;.json

```json
{
 "banque": 1,
 "item": "193",
 "titre": "Vascularites systémiques…",
 "maj": "2026-11-13",
 "sources": {
  "S1": {"type": "college", "titre": "Collège de Médecine interne", "edition": "5e éd. actualisée"},
  "S2": {"type": "lisa", "titre": "Fiche LiSA de l'item 193", "item": "193", "consulte": "2026-10"}
 },
 "dossiers": [
  {"id": "193-D01", "type": "DP", "enonce": "Mme R., 67 ans…", "questions": ["193-0027", "193-0028"],
   "origine": {"serie": "193-J30", "bloc": "DP1"}}
 ],
 "questions": [
  {"id": "193-0001", "v": 1, "type": "QRM", "dossier": null,
   "enonce": "…", "propositions": [{"l": "A", "t": "…", "statut": "vrai", "ok": true, "exp": "Vrai. …"}],
   "objectif": {"code": "OIC-193-01", "rang": "A", "libelle": "…"}, "hors_objectifs": null,
   "contexte": "…", "raisonnement": "…", "remarque": "",
   "src": ["S1", "S2"], "confiance": "non_relue", "prio": [],
   "cree": "2026-10-14", "origine": {"serie": "193-J1", "n": 1}}
 ]
}
```

### Une question

Une question de banque est une question de série au format 2 (voir `FORMAT.md` : `type`, `enonce`, `propositions`, `n_attendu`, `qroc`, `tcs`, `qzp`, `images`, `objectif`, `hors_objectifs`, `contexte`, `raisonnement`, `remarque`), sans `n` ni `bloc`, avec en plus :

- `id` : identifiant définitif, `<item>-<numéro sur 4 chiffres>`. Il n'est jamais réutilisé ni modifié : la progression des étudiants, les signalements et les confirmations s'y rattachent.
- `v` : version, à partir de 1. Elle augmente quand la correction change le sens de la question ou sa réponse (voir « Corriger une question »).
- `dossier` : identifiant du dossier auquel la question appartient, ou `null`.
- `src` : sources de la question, clés du champ `sources` du fichier.
- `confiance` : `non_relue`, `confirmee` (validée par un relecteur de confiance) ou `corrigee` (corrigée après signalement).
- `prio` : relecture prioritaire. `dose_seuil` (une dose ou un seuil figure dans les propositions ou la réponse attendue), `urgence`. Liste vide sinon. Posé automatiquement, modifiable à la main.
- `cree` : date de rédaction.
- `origine` : série et numéro d'où vient la question (questions versées depuis des séries personnelles). Sert à rattacher d'anciens résultats.
- `retiree` (facultatif) : `true` pour une question retirée. Elle reste dans le fichier, n'est plus proposée, et son identifiant n'est pas réattribué.
- `historique` (facultatif) : `[{"v": 2, "date": "2026-12-01", "motif": "dose_seuil", "note": "Seuil corrigé d'après…", "signalements": [12]}]`.

### Un dossier

`id` (`<item>-D<numéro>`), `type` (`DP`, `KFP` ou `TCS`), `enonce`, `images` (facultatif), `questions` (identifiants, dans l'ordre). Un dossier se tire toujours en entier et dans l'ordre. Ses questions sont toutes rangées dans le même fichier que lui, même quand leur objectif relève d'un autre item.

### Où ranger une question

- Dans le fichier de l'item de son objectif : `OIC-047-32` va dans `banque/47.json`.
- Question d'un dossier : dans le fichier du dossier (l'item le plus représenté parmi ses questions).
- Question hors objectifs : dans le fichier de l'item qu'elle complète.

### Sources

`type` : `college` (`titre`, `edition`), `lisa` (`item`, `consulte` : mois de consultation), `cours` (`titre`, `url`, `consulte`), `reco` (recommandation d'une société savante ou de la HAS : `titre`, `annee`, `url`). Les questions et leurs corrections sont rédigées avec nos propres mots : ni tableau, ni figure, ni photo repris d'un collège ou de LiSA.

## Niveau de confiance affiché

Le site combine le champ `confiance` du fichier et les compteurs publics de la base (`questions_etat`, pour la même `question_id` et la même `version`). Sans connexion à la base, seul le champ du fichier compte.

1. **Signalée** : au moins un signalement ouvert dans la base.
2. **Corrigée** : `confiance` vaut `corrigee`.
3. **Confirmée** : `confiance` vaut `confirmee`, ou au moins une confirmation d'un relecteur dans la base.
4. **Non relue** : sinon. Le nombre de confirmations d'étudiants peut s'afficher à côté.

## Corriger une question

- Faute de forme (orthographe, tournure) : corriger le texte, ne pas changer `v`.
- Correction de fond (réponse, proposition, dose, seuil, source) : corriger, augmenter `v` de 1, passer `confiance` à `corrigee`, ajouter une ligne à `historique`, puis clore les signalements dans la base. Les compteurs de la nouvelle version repartent de zéro.
- Ne jamais supprimer une question : la marquer `retiree`.

## banque/index.json

```json
{"banque": 1, "maj": "2026-11-13", "total": {"q": 823, "dossiers": 104},
 "items": {"193": {"titre": "…", "maj": "2026-11-13", "q": 42, "dossiers": 4, "hors_objectifs": 6,
   "prioritaires": 3, "confiance": {"non_relue": 42}, "octets": 114352,
   "objectifs": {"OIC-193-01": {"rang": "A", "q": 3}}}}}
```

Il est recalculé par les outils, jamais écrit à la main.

## Outils (dépôt de données)

- `outils/migrer_banque.py <dépôt de données> <dossier banque>` : verse les séries de `data/series/` dans la banque. Incrémental : une question déjà versée est ignorée, les identifiants existants ne bougent pas.
- `outils/verifier_banque.py <dossier banque> [<dépôt de données>]` : contrôle les identifiants, les types, les réponses, les dossiers, les sources et les doublons. À lancer avant toute publication.
