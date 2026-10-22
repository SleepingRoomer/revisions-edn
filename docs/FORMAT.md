# Format des données

Le site lit un dépôt GitHub de données (de préférence **privé**) organisé ainsi :

```
data/<collection>/<id>.json
```

Un fichier = un document JSON (UTF-8). Le site charge tout le dossier `data/` en une requête, puis écrit chaque document séparément (un commit par enregistrement). Tout outil qui produit des fichiers à ce format (Claude, un script, un autre modèle, ou toi à la main) alimente le site.

## items/&lt;id&gt;.json : une fiche

```json
{
  "num": "193",
  "titre": "Vascularites systémiques",
  "specialite": "Médecine interne",
  "source": "Collège de Médecine interne + fiche LiSA",
  "fiche_url": "https://docs.google.com/document/d/…/edit",
  "cours_url": "",
  "date_fiche": "2026-10-13",
  "objectifs_docs": [{"titre": "Objectifs LiSA – item 193", "url": "https://docs.google.com/…"}],
  "items_lisa": ["193"],
  "objectifs": [{"item": "193", "code": "OIC-193-01", "rang": "A", "rubrique": "Définition", "libelle": "Définition d'une vascularite"}],
  "ordre": 8,
  "college": "medecine-interne"
}
```

- `id` (nom du fichier) : le numéro d'item, ou un identifiant libre quand une fiche regroupe plusieurs items (`suivi`, `depistages`).
- `num` : texte affiché (« 193 » ou « 47 · 59 · 256 »).
- `items_lisa` : numéros d'items EDN couverts (pour la carte des 367 items et les collèges).
- `objectifs` : objectifs de connaissance (programme officiel), utilisés par l'onglet Suivi.
- `titre_doc` et `notes_qcm` : titre court des Google Docs et consignes propres à l'item pour la rédaction des séries.
- `college` : identifiant d'un document `colleges/` ; le chapitre portant le même numéro d'item est alors compté comme fait.
- `ordre` : ordre d'affichage.

## series/&lt;item&gt;-&lt;J&gt;.json : une série de QCM

Créée d'avance avec `"statut": "planifiee"` et `"questions": []`, puis remplacée par la série complète le jour prévu. `serie` vaut `J` suivi du nombre de jours depuis la fiche : `J1`, `J7`, `J30`, puis les séries programmées selon les résultats (`J75`, `J105`…), qui portent aussi `phase` (`adaptatif` ou `finale`), `intervalle`, `motif` et `cibles` (objectifs à retravailler).

### Format 2 (épreuves dématérialisées R2C)

```json
{
  "version": 2, "item": "48", "serie": "J7", "date": "2026-10-29",
  "doc_url": "https://docs.google.com/document/d/…/edit",
  "titre": "QCM J7 – Item 48 Alimentation du nourrisson et de l'enfant",
  "statut": "disponible",
  "blocs": [{"id": "DP1", "type": "DP", "enonce": "Énoncé initial du dossier"}],
  "questions": [
    {"n": 1, "type": "QRU", "bloc": null, "enonce": "…",
     "propositions": [{"l": "A", "t": "…", "statut": "indispensable", "ok": true, "exp": "Vrai. …"},
                      {"l": "B", "t": "…", "statut": "inacceptable", "ok": false, "exp": "Faux. …"}],
     "objectif": {"code": "OIC-048-03", "rang": "A", "libelle": "…"}, "hors_objectifs": null,
     "contexte": "…", "raisonnement": "…", "remarque": ""},
    {"n": 2, "type": "QROC", "propositions": [],
     "qroc": {"exactes": ["lait de croissance"], "acceptables": ["lait infantile"], "consigne": "Réponse attendue en un à cinq mots, sans abréviation", "numerique": false}},
    {"n": 3, "type": "TCS", "bloc": "TCS1", "enonce": "", "propositions": [],
     "tcs": {"hypothese": "…", "information": "…", "echelle": "diagnostic", "panel": [2, 13, 5, 0, 0]}}
  ]
}
```

- `type` : `QRM`, `QRU`, `QRP` (4 ou 5 propositions, `n_attendu`), `QRPL` (QRP longue, 10 à 25 propositions, `n_attendu`), `QROC`, `TCS`. Une question sans `type` (format 1) est une QRM.
- `statut` d'une proposition : `vrai`, `faux`, `indispensable` (l'oublier donne 0) ou `inacceptable` (la cocher donne 0) ; `ok` vaut `true` pour `vrai` et `indispensable`.
- Blocs : `DP` (dossier progressif : les questions se débloquent l'une après l'autre et ne se modifient plus une fois validées en conditions d'épreuve), `KFP`, `TCS` (3 questions sur un même énoncé).
- Notation (règles du CNG 2024-2025) : QRM par discordances (0 = 1 point, 1 = 0,5, 2 = 0,2, 3 et plus = 0) ; QRU binaire ; QRP et QRP longue en x/n ; QROC 1 (réponse exacte), 0,5 (acceptable) ou 0, abréviations hors liste du conseil scientifique comptées fausses, avec auto-correction possible ; TCS selon le panel (ancrage modal = 1, autres = effectif / effectif modal).
- Note validante : moyenne des questions de rang A en QRU, QRP et QROC, sur 20 (seuil de 14/20).
- Question hors objectifs : `"objectif": null` et `"hors_objectifs"` renseigné (`hors_lisa` est encore lu pour les anciennes séries).

## resultats/&lt;serie&gt;_&lt;horodatage&gt;.json : une tentative

Écrit par le site à la fin d'une épreuve : `serie_id`, `item`, `serie`, `date`, `debut`, `duree_s`, `mode` (`epreuve` ou `entrainement`), `points`, `max`, `reponses` (`n`, `type`, `choix` : lettres, texte de QROC ou ancrage de TCS, `correct`, `disc`, `pts`, `ov` : note retenue en auto-correction de QROC, `objectif`, `rang`, `validante`, `hors_objectifs`).

## relectures/&lt;serie&gt;.json

`{"item": "193", "serie": "J1", "fait": true, "date": "…"}` : relecture de la fiche cochée.

## carnet/&lt;id&gt;.json : carnet d'erreurs

Trois types :
- question entière (`<serie>__q<n>`) : `question` (copie de la question), `choix`, `pts` ;
- proposition isolée (`<serie>__q<n>__<lettre>`, `"type": "proposition"`) : `enonce`, `prop`, `choisie`, `juste` ;
- item entier (`item__<id>`, `"type": "item"`) : `num`, `titre`.

Champs communs : `note`, `statut` (`a_revoir` ou `maitrisee`), `ajoute`, `revues` (historique des révisions).

## colleges/&lt;id&gt;.json

`{"nom", "edition", "ordre", "chapitres": [{"id", "chapitre", "titre", "items": [193], "rubrique", "fiches": ["193"], "url"}]}`

## progression/&lt;college&gt;.json

`{"chapitres": {"<id du chapitre>": {"fait": true, "date": "…"}}}` : chapitres marqués faits sans fiche.

## planning/&lt;id&gt;.json (facultatif)

`{"titre", "promo", "annee", "site", "events": [{"id", "date", "debut", "fin", "libelle", "matiere", "salle", "site", "type"}]}`
