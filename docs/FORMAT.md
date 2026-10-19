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
- `objectifs` : objectifs LiSA, utilisés par l'onglet Suivi.
- `college` : identifiant d'un document `colleges/` ; le chapitre portant le même numéro d'item est alors compté comme fait.
- `ordre` : ordre d'affichage.

## series/&lt;item&gt;-&lt;J&gt;.json : une série de QCM

Créée d'avance avec `"statut": "planifiee"` et `"questions": []`, puis remplacée par la série complète le jour prévu.

```json
{
  "item": "193", "serie": "J7", "date": "2026-10-20",
  "doc_url": "https://docs.google.com/document/d/…/edit",
  "titre": "QCM J7 – Item 193 Vascularites",
  "statut": "disponible",
  "questions": [
    {
      "n": 1,
      "enonce": "Énoncé ou vignette clinique",
      "propositions": [
        {"l": "A", "t": "Texte", "ok": true, "exp": "Vrai. Explication"},
        {"l": "B", "t": "Texte", "ok": false, "exp": "Faux. Explication"}
      ],
      "objectif": {"code": "OIC-193-04", "rang": "B", "libelle": "Diagnostics différentiels"},
      "hors_lisa": null,
      "contexte": "Situation clinique générale et ce que la question teste.",
      "raisonnement": "Démarche, indice discriminant, pièges.",
      "remarque": ""
    }
  ]
}
```

- 5 propositions A à E, une ou plusieurs vraies. Notation EDN par discordances : 0 = 1 point, 1 = 0,5, 2 = 0,2, 3 et plus = 0.
- Question hors LiSA : `"objectif": null` et `"hors_lisa": "collège"` ou `"cours CNPU"`.
- `serie` : `J1`, `J7` ou `J30`. `date` : jour où la série devient « du jour ».

## resultats/&lt;serie&gt;_&lt;horodatage&gt;.json : une tentative

Écrit par le site à la fin d'une épreuve : `serie_id`, `item`, `serie`, `date`, `debut`, `duree_s`, `mode` (`epreuve` ou `entrainement`), `points`, `max`, `reponses` (`n`, `choix`, `correct`, `disc`, `pts`, `objectif`, `rang`, `hors_lisa`).

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
