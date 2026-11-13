# Format des données

Le site range ses données soit dans le navigateur (mode par défaut, sans compte), soit dans un dépôt GitHub de données (de préférence **privé**). Dans les deux cas, ce sont les mêmes documents, organisés ainsi :

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
  "college": "medecine-interne",
  "annales": [{"annee": 2025, "epreuve": "Épreuve dématérialisée 2025 · R1", "bloc": "QI 36", "theme": "Rhinite croûteuse et otite : granulomatose avec polyangéite", "place": "central"}]
}
```

- `id` (nom du fichier) : le numéro d'item, ou un identifiant libre quand une fiche regroupe plusieurs items (`suivi`, `depistages`).
- `num` : texte affiché (« 193 » ou « 47 · 59 · 256 »).
- `items_lisa` : numéros d'items EDN couverts (pour la carte des 367 items et les collèges).
- `objectifs` : objectifs de connaissance (programme officiel), utilisés par l'onglet Suivi.
- `titre_doc` et `notes_qcm` : titre court des Google Docs et consignes propres à l'item pour la rédaction des séries.
- `college` : identifiant d'un document `colleges/` ; le chapitre portant le même numéro d'item est alors compté comme fait.
- `ordre` : ordre d'affichage.
- `iconographies` : images de la fiche, affichées dans l'encadré « Iconographies » et utilisables dans les questions :
  `[{"id": "I1", "titre": "Purpura vasculaire des membres inférieurs", "legende": "Purpura infiltré, déclive…", "url": "https://…/image.jpg", "objectif": "OIC-193-07", "exigible": true, "source_url": "https://…", "credit": "…"}]`.
  `id` : `I` suivi d'un nombre, unique dans la fiche. `url` : adresse https de l'image, image enregistrée dans le navigateur (`data:image/jpeg;base64,…`, mode sans compte) ou `repo:images/<item>/<fichier>.jpg` (fichier du dépôt de données, hors de `data/`, lu avec la clé GitHub). `objectif` : code de l'objectif illustré. `exigible` : image attendue par un objectif « contenu multimédia » ; si le champ est absent, le site le déduit de la rubrique et du libellé de l'objectif (ou de son champ `multimedia`, `true` ou `false`). Les objectifs multimédia sans image sont listés sur la fiche comme « images attendues ».
  `zones` (facultatif) : zones à pointer de l'image, pour les QZP : `[{"id": "Z1", "nom": "trait de fracture", "x": 0.31, "y": 0.42, "w": 0.12, "h": 0.2}]`. Rectangle en fractions de l'image (0 à 1), `x` et `y` désignant son coin haut gauche. Elles se tracent sur le site : image de la fiche › « Zones à pointer ».
- `annales` : blocs ou questions des épreuves nationales 2023 à 2026 qui portent sur l'item (`place` : `central` ou `partiel` quand l'item n'occupe qu'une partie du bloc). Affichés sous la fiche (« Aux annales ») et lus avant de rédiger une série. Une liste vide signifie que l'item n'est jamais tombé ; champ absent : pas encore recherché.

## fiches/&lt;id&gt;.json : le texte d'une fiche, lu sur le site (facultatif)

Quand ce document existe, « Ouvrir la fiche » affiche la fiche sur le site (page `#fiche/<id>`) au lieu d'ouvrir `fiche_url`.

```json
{
  "item": "193", "titre": "Item 193 : Vascularites systémiques", "intro": "Fiche de révision d'après…",
  "source_doc": "https://docs.google.com/document/d/…/edit", "maj": "2026-11-12",
  "sections": [
    {"id": "s4", "titre": "Purpura vasculaire", "rang": "A", "objectifs": ["OIC-193-06", "OIC-193-07"],
     "blocs": [
       {"type": "p", "t": "Texte, avec **gras** possible."},
       {"type": "h3", "t": "Sous-titre"},
       {"type": "ul", "items": [{"t": "Libellé : contenu", "sub": [{"t": "sous-point"}]}]},
       {"type": "table", "head": ["Calibre", "Vaisseaux"], "rows": [["Gros", "Aorte…"]]},
       {"type": "img", "ref": "I1"},
       {"type": "note", "titre": "À ne pas rater", "t": "…"}
     ]}
  ]
}
```

- `objectifs` d'une section : la section affiche l'état de ces objectifs (acquis, fragile, à revoir), le nombre d'erreurs aux QCM et, à la fin, les iconographies de la fiche rattachées à ces objectifs (sauf celles déjà placées par un bloc `img`).
- `type` d'une section (facultatif) : `retenir`, `raisonnement`, `sources`, `complement`, pour la mise en forme.
- Dans une liste, le libellé avant « : » est mis en gras automatiquement.
- Le dépôt de données fournit `outils/convertir_fiche.py`, qui produit ce fichier à partir de l'export HTML d'un Google Doc sans en changer le texte.

- `modifie` : date de la dernière modification faite sur le site (bouton « Modifier » d'une section). Le convertisseur ne remplace pas une fiche modifiée sans l'option `--force`.

## annotations/&lt;id&gt;.json : surlignages et commentaires d'une fiche

`{"item": "193", "a": [{"id": "a…", "p": "s4/0/1", "s": 12, "e": 48, "q": "infiltré (palpable), confluent", "c": "j", "note": "tombé en 2025", "date": "…"}]}`

- `p` : chemin du texte annoté (section / bloc / élément ; `h0`, `r2c1` pour une cellule de tableau). `s`, `e` : positions dans ce texte ; `q` : passage surligné, qui sert à le retrouver quand le texte change. `c` : `j` jaune, `v` vert, `r` rose, `b` bleu. `note` : commentaire.
- Une note de section a `p` égal à l'identifiant de la section, sans `s`, `e` ni `q`.

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

- `type` : `QRM`, `QRU`, `QRP` (4 ou 5 propositions, `n_attendu`), `QRPL` (QRP longue, 10 à 25 propositions, `n_attendu`), `QROC`, `TCS`, `QZP`.
- QZP (zone à pointer) : `"propositions": []`, une seule image dans `images`, et `"qzp": {"cibles": [{"zone": "Z1", "nom": "trait de fracture", "x": 0.31, "y": 0.42, "w": 0.12, "h": 0.2}]}` (coordonnées recopiées de la zone de la fiche ; une cible par pointeur à placer). L'étudiant clique sur l'image ; un pointeur dans le rectangle compte juste. Note : zones trouvées / zones attendues. La réponse enregistrée est « x,y » par cible, séparées par « ; ». Une question sans `type` (format 1) est une QRM.
- `statut` d'une proposition : `vrai`, `faux`, `indispensable` (l'oublier donne 0) ou `inacceptable` (la cocher donne 0) ; `ok` vaut `true` pour `vrai` et `indispensable`.
- Blocs : `DP` (dossier progressif : les questions se débloquent l'une après l'autre et ne se modifient plus une fois validées en conditions d'épreuve), `KFP`, `TCS` (3 questions sur un même énoncé).
- Notation (règles du CNG 2024-2025) : QRM par discordances (0 = 1 point, 1 = 0,5, 2 = 0,2, 3 et plus = 0) ; QRU binaire ; QRP et QRP longue en x/n ; QROC 1 (réponse exacte), 0,5 (acceptable) ou 0, abréviations hors liste du conseil scientifique comptées fausses, avec auto-correction possible ; TCS selon le panel (ancrage modal = 1, autres = effectif / effectif modal).
- Note validante : moyenne des questions de rang A en QRU, QRP et QROC, sur 20 (seuil de 14/20).
- Image : une question ou un bloc peut porter `"images": [{"item": "193", "ref": "I1"}]`, renvoi à une iconographie de la fiche (`ref` = son `id`). L'image s'affiche sous l'énoncé et s'agrandit d'un clic ; son titre et sa légende n'apparaissent qu'à la correction. Une image hors fiche s'écrit `{"url": "https://…", "titre": "…", "legende": "…"}`.
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

## reglages/prefs.json : réglages de l'étudiant (page « Mes outils »)

`{"profil": "edn", "outils": {"carnet": true, "erreurs": true, "suivi": true, "icono": true, "annot": false, "colleges": false, "planning": false}, "rythme": [1, 7, 30], "relec": 7, "secq": 90, "taille": 1, "dys": false, "theme": "auto"}`

- `outils` : outils affichés ; champ absent = tous. `rythme` : jours des séries créées avec une nouvelle fiche. `relec` : la relecture de la fiche est demandée pour les séries jusqu'à ce jour (0 : jamais ; 9999 : toujours). `secq` : secondes par question en conditions d'épreuve. `taille` : 0.9, 1, 1.12 ou 1.25. `theme` : `auto`, `clair`, `sombre`.

## colleges/&lt;id&gt;.json

`{"nom", "edition", "ordre", "chapitres": [{"id", "chapitre", "titre", "items": [193], "rubrique", "fiches": ["193"], "url"}]}`

## progression/&lt;college&gt;.json

`{"chapitres": {"<id du chapitre>": {"fait": true, "date": "…"}}}` : chapitres marqués faits sans fiche.

## planning/&lt;id&gt;.json (facultatif)

`{"titre", "promo", "annee", "site", "events": [{"id", "date", "debut", "fin", "libelle", "matiere", "salle", "site", "type"}]}`

## Sauvegarde (mode sans compte)

Le bouton « Sauvegarder dans un fichier » produit `revisions-edn-sauvegarde-<date>.json` :
`{"app": "revisions-edn", "version": 1, "exporte": "<date ISO>", "nom": "…", "docs": {"items/48": {…}, "series/48-J1": {…}, …}}`. « Restaurer une sauvegarde » remplace toutes les données de l'appareil par celles du fichier.

## Format texte des séries préparées avec une IA

La page « Préparer la série » copie une consigne qui demande ce format, puis le convertit en série au format 2 :

```text
=== DP1 · DP ===
Énoncé : énoncé initial du dossier.

=== Q1 · QRM · O2 ===
Bloc : DP1
Énoncé : texte de la question.
Image : I1
A. [V] proposition vraie
Explication : pourquoi.
B. [F] proposition fausse
Explication : pourquoi.
Contexte : rappel de cours.

=== Q2 · QROC · O4 ===
Énoncé : …
Réponses exactes : réponse ; synonyme
Réponses acceptables : aucune
Explication : …

=== Q3 · TCS · O3 ===
Bloc : TCS1
Hypothèse : …
Information : …
Échelle : diagnostic
Panel : 2 / 13 / 5 / 0 / 0
Explication : …
```

- `[V]` vrai, `[F]` faux, `[V!]` indispensable, `[F!]` inacceptable. En QRU, la proposition vraie devient indispensable et les autres inacceptables ; en QRP longue, seuls vrai et faux sont gardés.
- QZP : `=== Q4 · QZP · O3 ===`, `Énoncé : Pointez…`, `Image : I1`, `Zones : Z1` (ou `Zones : Z1, Z2`), `Explication : …`. Les zones doivent exister sur l'image de la fiche.
- `Image : I1` (ou `Image : I1, I2`), sous l'énoncé d'une question ou d'un bloc, renvoie aux iconographies de la fiche ; une image inconnue fait refuser la série.
- `O2` renvoie au 2e objectif de l'item (`OIC-<item>-02`), `HO` à une question hors objectifs.
- L'analyse tolère le gras Markdown, les titres `### Q1 · …`, les lettres `A)` et un texte d'introduction. Elle refuse une série dont une question n'a pas d'énoncé, pas de proposition vraie, plusieurs vraies en QRU, pas de réponse exacte en QROC ou un panel incomplet en TCS.
