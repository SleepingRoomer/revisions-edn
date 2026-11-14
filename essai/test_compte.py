#!/usr/bin/env python3
"""Parcours complet du compte dans un navigateur, en mode « sur cet appareil », contre une fausse base
(mêmes adresses, mêmes colonnes autorisées que la vraie). Usage : test_compte.py <adresse du site>"""
import base64, json, re, sys, time, urllib.parse
from playwright.sync_api import sync_playwright

SITE = sys.argv[1].rstrip("/") + "/"
SB = "https://kwfdvshewnjbnguhaodt.supabase.co"
KEY = "sb_publishable_R4XLYx0koHMdSiKLtenw5w_cXUssK11"
UID = "11111111-2222-3333-4444-555555555555"
ok = 0

def check(cond, label):
    global ok
    if not cond:
        raise AssertionError(label)
    ok += 1
    print("  ok :", label)

def b64(o):
    return base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip("=")

class Base:
    """Fausse base : contrôle les en-têtes et les colonnes envoyées, comme les droits de la vraie."""
    def __init__(self):
        self.docs = {}; self.profil = None; self.sig = []; self.conf = set(); self.seq = 0; self.clock = 0
        self.tokens = set(); self.refresh = {}; self.log = []; self.fail = []; self.n_refresh = 0; self.expire = set()
    def now(self):
        self.clock += 1
        return "2026-11-14T10:%02d:%02d.%06d+00:00" % (self.clock // 60, self.clock % 60, self.clock)
    def session(self):
        self.seq += 1
        at = "h." + b64({"sub": UID, "email": "lea@exemple.fr", "exp": int(time.time()) + 3600, "n": self.seq}) + ".s"
        rt = "rt%d" % self.seq
        self.tokens.add(at); self.refresh[rt] = 1
        return {"access_token": at, "refresh_token": rt, "expires_in": 3600, "token_type": "bearer", "user": {"id": UID, "email": "lea@exemple.fr"}}
    def bad(self, msg):
        self.fail.append(msg)
    def handle(self, route):
        rq = route.request
        if rq.method == "OPTIONS":
            return route.fulfill(status=204, headers={"access-control-allow-origin": "*", "access-control-allow-headers": "*", "access-control-allow-methods": "*"})
        u = urllib.parse.urlsplit(rq.url); q = urllib.parse.parse_qs(u.query); path = u.path; hd = rq.headers
        body = json.loads(rq.post_data) if rq.post_data else None
        self.log.append((rq.method, path, u.query))
        def out(status, data=None):
            return route.fulfill(status=status, headers={"access-control-allow-origin": "*", "content-type": "application/json"}, body="" if data is None else json.dumps(data))
        if hd.get("apikey") != KEY: self.bad("clé absente : " + path)
        auth = hd.get("authorization", "")
        if auth == "Bearer " + KEY: self.bad("clé publique envoyée dans Authorization : " + path)
        tok = auth[7:] if auth.startswith("Bearer ") else None
        user = tok is not None and tok in self.tokens and tok not in self.expire
        def eq(k):
            v = q.get(k, [None])[0]
            return v[3:] if v and v.startswith("eq.") else None
        def inl(k):
            v = q.get(k, [None])[0]
            return v[4:-1].split(",") if v and v.startswith("in.(") else None
        def cols(allowed):
            extra = set(body or {}) - set(allowed)
            if extra: self.bad("%s %s : colonnes non autorisées %s" % (rq.method, path, sorted(extra)))
        # --- connexion ---
        if path == "/auth/v1/otp":
            if "redirect_to" not in q: self.bad("redirect_to absent")
            return out(200, {})
        if path == "/auth/v1/verify":
            return out(200, self.session()) if body.get("token") == "123456" and body.get("type") == "email" else out(403, {"code": 403, "error_code": "otp_expired", "msg": "Token has expired or is invalid"})
        if path == "/auth/v1/token":
            self.n_refresh += 1
            if self.refresh.pop(body.get("refresh_token"), None): return out(200, self.session())
            return out(400, {"error_code": "refresh_token_not_found", "msg": "Invalid Refresh Token"})
        if path == "/auth/v1/logout": return out(204)
        # --- lecture publique ---
        if path == "/rest/v1/facultes": return out(200, [{"id": "lille", "nom": "Lille"}, {"id": "autre", "nom": "Autre"}])
        if path == "/rest/v1/questions_etat":
            ids = inl("question_id") or []; res = []
            for i in ids:
                s = sum(1 for x in self.sig if x["question_id"] == i and x["statut"] == "ouvert"); c = sum(1 for (a, v) in self.conf if a == i)
                if s or c: res.append({"question_id": i, "version": 1, "signalements_ouverts": s, "confirmations": c, "confirmations_relecteurs": 0})
            return out(200, res)
        if tok is not None and not user: return out(401, {"code": "PGRST301", "message": "JWT expired"})
        if not user: return out(401, {"code": "42501", "message": "permission denied"})
        # --- au nom de l'étudiant ---
        if path == "/rest/v1/relecteurs": return out(200, [])
        if path == "/rest/v1/profils":
            if rq.method == "GET": return out(200, [self.profil] if self.profil else [])
            cols(["pseudo", "faculte", "annee_edn", "classements"])
            if re.search(r"insulte", body["pseudo"], re.I): return out(400, {"code": "23514", "message": "PSEUDO_REFUSE : ce pseudo n'est pas accepté"})
            if rq.method == "POST" and self.profil: return out(409, {"code": "23505", "message": "duplicate key"})
            self.profil = dict(self.profil or {}, **body, pseudo_modifie_le=self.now()); return out(201 if rq.method == "POST" else 200, [self.profil])
        if path == "/rest/v1/documents":
            if rq.method == "GET":
                after = (q.get("updated_at", ["gt."])[0])[3:]
                rows = sorted((d for d in self.docs.values() if d["updated_at"] > after), key=lambda d: d["updated_at"])
                return out(200, rows)
            if rq.method == "POST":
                cols(["collection", "doc_id", "data", "supprime"]); k = (body["collection"], body["doc_id"])
                if body["collection"] not in ("memoire", "progression", "reglages", "annotations", "carnet", "relectures"): return out(400, {"code": "23514", "message": "collection refusée"})
                if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$", body["doc_id"]): return out(400, {"code": "23514", "message": "doc_id refusé"})
                if k in self.docs: return out(409, {"code": "23505", "message": "duplicate key"})
                self.docs[k] = dict(body, updated_at=self.now()); return out(201, [self.docs[k]])
            if rq.method == "PATCH":
                cols(["data", "supprime"]); k = (eq("collection"), eq("doc_id"))
                if k not in self.docs: return out(200, [])
                self.docs[k].update(body, updated_at=self.now()); return out(200, [self.docs[k]])
        if path == "/rest/v1/signalements":
            if rq.method == "GET":
                ids = inl("question_id"); st = eq("statut")
                return out(200, [x for x in self.sig if (ids is None or x["question_id"] in ids) and (st is None or x["statut"] == st)])
            if rq.method == "POST":
                cols(["question_id", "version", "item", "motif", "commentaire"])
                if any(x["question_id"] == body["question_id"] and x["statut"] == "ouvert" for x in self.sig): return out(409, {"code": "23505", "message": "duplicate key"})
                row = dict(body, id=len(self.sig) + 1, statut="ouvert", reponse=None, created_at=self.now()); self.sig.append(row); return out(201, [row])
            if rq.method == "DELETE":
                self.sig = [x for x in self.sig if str(x["id"]) != eq("id")]; return out(204)
        if path == "/rest/v1/confirmations":
            if rq.method == "GET":
                ids = inl("question_id") or []; return out(200, [{"question_id": a, "version": v} for (a, v) in self.conf if a in ids])
            if rq.method == "POST":
                cols(["question_id", "version", "item"]); self.conf.add((body["question_id"], body["version"])); return out(201)
            if rq.method == "DELETE":
                self.conf.discard((eq("question_id"), int(eq("version")))); return out(204)
        self.bad("appel imprévu : %s %s" % (rq.method, path)); return out(404, {"message": "inconnu"})

IDB = """() => new Promise((res, rej) => { const r = indexedDB.open("revisions-edn", 1); r.onsuccess = () => { const st = r.result.transaction("docs").objectStore("docs");
  const k = st.getAllKeys(), v = st.getAll(); v.onsuccess = () => { const o = {}; k.result.forEach((x, i) => o[x] = v.result[i]); res(o) } }; r.onerror = () => rej(r.error) })"""

def device(browser, base, errors, name):
    ctx = browser.new_context(viewport={"width": 1200, "height": 900})
    ctx.route(SB + "/**", base.handle)
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(name + " : " + str(e)))
    page.on("console", lambda m: errors.append(name + " console : " + m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)
    page.on("dialog", lambda d: d.accept())
    return ctx, page

def seance(page, n=3):
    page.goto(SITE + "#seance"); page.wait_for_selector("text=Mes items")
    if page.locator("input.otog:checked").count() == 0:
        page.click("text=Tout cocher")
    inp = page.locator('input[aria-label="Nombre exact de questions"]').first
    inp.fill(str(n)); inp.dispatch_event("change")
    page.goto(SITE + "#today"); page.click("button:has-text('Commencer la séance'), button:has-text('Faire une séance libre')")
    page.wait_for_selector(".exam")
    page.locator("button:has-text('Terminer')").first.click()
    page.locator(".modal button.salmon").click()
    page.wait_for_selector("text=Séance enregistrée")

def wait_sync(page, base, cond, label, t=15):
    end = time.time() + t
    while time.time() < end:
        if cond(): return check(True, label)
        page.wait_for_timeout(250)
    check(False, label)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    base = Base(); errors = []

    print("Appareil A, sans compte")
    ctxA, A = device(browser, base, errors, "A")
    A.goto(SITE); A.click("button:has-text('Commencer')"); A.wait_for_selector("text=Bienvenue")
    check(A.locator("#foot button:has-text(\"Mettre mes révisions à l'abri\")").count() == 1, "le pied de page propose de mettre ses révisions à l'abri")
    A.goto(SITE + "#outils"); A.click("button.ocard:has-text('Tout')")
    seance(A)
    check(not base.docs, "rien n'est envoyé sans compte")
    A.click("text=Voir la correction"); A.wait_for_selector("text=Signaler une erreur")
    check(A.locator(".tag:has-text('Non relue')").count() >= 1, "niveau de confiance du fichier affiché")
    check(any(pth == "/rest/v1/questions_etat" for (_, pth, _) in base.log), "compteurs publics demandés sans compte")
    A.click("text=Signaler une erreur"); A.wait_for_selector("text=Un compte est nécessaire")
    A.click("text=Créer mon compte ou me connecter"); A.wait_for_selector("text=Créer mon compte ou me connecter >> nth=0")
    check("#compte" in A.url, "renvoi vers l'écran du compte")

    print("Connexion et pseudo")
   
    A.fill('input[type="email"]', "pas une adresse"); A.click("text=Recevoir le lien de connexion"); A.wait_for_selector("text=Écris une adresse mail valide")
    A.fill('input[type="email"]', "Lea@Exemple.fr"); A.click("text=Recevoir le lien de connexion"); A.wait_for_selector("text=Regarde tes mails")
    A.fill('input[aria-label="Code reçu par mail"]', "000000"); A.click("button:has-text('Valider')"); A.wait_for_selector("text=Code refusé")
    A.fill('input[aria-label="Code reçu par mail"]', "123456"); A.click("button:has-text('Valider')"); A.wait_for_selector("text=Choisis ton pseudo")
    A.goto(SITE + "#today"); A.wait_for_timeout(300)
    check(A.locator("text=Choisis ton pseudo").count() == 1, "sans pseudo, le site ne laisse pas continuer")
    check(not base.docs, "rien n'est copié avant le pseudo")
    A.fill('input[aria-label="Pseudo"]', "Insulte"); A.click("text=Créer mon profil"); A.wait_for_selector("text=Ce pseudo n'est pas accepté")
   
    A.fill('input[aria-label="Pseudo"]', "Léa M"); A.select_option('select[aria-label="Faculté"]', "lille"); A.click("text=Créer mon profil")
    wait_sync(A, base, lambda: ("reglages", "prefs") in base.docs and any(k[0] == "memoire" for k in base.docs), "première copie : réglages et mémoire des séances envoyés")
    A.goto(SITE + "#compte"); A.wait_for_selector("text=Tout est à l'abri")
    check(A.locator("h2:has-text('Léa M')").count() == 1 and A.locator("text=Lille").count() >= 1, "profil affiché")
    locA = A.evaluate(IDB)
    mem_keys = sorted(k for k in locA if k.startswith("memoire/"))
    check(all(base.docs[("memoire", k[8:])]["data"] == locA[k] for k in mem_keys) and mem_keys, "mémoire du compte identique à celle de l'appareil")
    check(not any(k[0] in ("resultats", "items", "series", "fiches") for k in base.docs), "fiches, séries et résultats restent sur l'appareil")

    print("Signalement, confirmation, carnet")
    rid = [k for k in locA if k.startswith("resultats/seance_")][0][10:]
    A.goto(SITE + "#correction/" + rid); A.wait_for_selector("text=Signaler une erreur")
    qid = A.locator(".xmain code").last.inner_text()
    A.click("text=Signaler une erreur"); A.wait_for_selector(".modal input[type=radio]")
    A.click("text=Envoyer le signalement"); A.wait_for_selector("text=Choisis ce qui ne va pas")
    A.check('input[value="dose_seuil"]'); A.fill(".modal textarea", "Le seuil indiqué ne correspond pas au collège."); A.click("text=Envoyer le signalement")
    A.wait_for_selector("text=Merci, ton signalement est enregistré"); A.click(".modal button:has-text('Fermer')")
    A.wait_for_selector("text=Tu as signalé cette question")
    check(A.locator(".tag:has-text('Signalée')").count() == 1, "la question passe à « Signalée »")
    A.locator("text=Tu as signalé cette question").scroll_into_view_if_needed();
    check(base.sig[0]["question_id"] == qid and base.sig[0]["motif"] == "dose_seuil" and base.sig[0]["version"] == 1, "signalement reçu avec la bonne question (" + qid + ")")
    A.click("text=Question suivante"); A.wait_for_selector("text=Elle me paraît juste")
    A.click("text=Elle me paraît juste"); A.wait_for_selector("text=Tu la juges juste")
    A.wait_for_selector("text=1 étudiant la juge juste")
    check(len(base.conf) == 1, "confirmation reçue")
    A.click("text=Tu la juges juste"); A.wait_for_selector("text=Elle me paraît juste"); check(len(base.conf) == 0, "confirmation retirée")
    qid2 = A.locator(".xmain code").last.inner_text()
    A.click("text=Ajouter au carnet"); A.wait_for_selector("text=Dans ton carnet d'erreurs")
    wait_sync(A, base, lambda: ("carnet", "banque__q" + qid2) in base.docs, "question du carnet copiée dans le compte")
    cd = base.docs[("carnet", "banque__q" + qid2)]["data"]
    check("question" not in cd and cd["n"] == qid2 and cd["v"] == 1, "le carnet part sans le texte de la question, avec son identifiant et sa version")
    A.goto(SITE + "#compte"); A.wait_for_selector("text=Mes signalements"); A.wait_for_selector("text=En cours d'examen")
    check(A.locator("text=Une dose ou un seuil est erroné").count() == 1, "« Mes signalements » liste le signalement")

    print("Appareil B : retour par le lien du mail")
    ctxB, B = device(browser, base, errors, "B")
    s = base.session()
    B.goto(SITE + "#access_token=%s&expires_in=3600&refresh_token=%s&token_type=bearer&type=magiclink" % (s["access_token"], s["refresh_token"]))
    B.wait_for_selector("text=Mon compte"); B.wait_for_selector("h2:has-text('Léa M')")
    check("access_token" not in B.url and B.url.endswith("#compte"), "les jetons ne restent pas dans l'adresse")
    wait_sync(B, base, lambda: any(k.startswith("carnet/") for k in B.evaluate(IDB)), "B reçoit la mémoire, les réglages et le carnet")
    locB = B.evaluate(IDB)
    check(all(locB.get(k) == locA[k] for k in mem_keys), "mémoire des séances identique sur B")
    check(locB["reglages/prefs"].get("profil") == "tout", "réglages retrouvés sur B")
    cb = locB["carnet/banque__q" + qid2]
    check(cb.get("question", {}).get("enonce") and cb["question"].get("propositions") is not None or cb["question"].get("qroc") is not None or cb["question"].get("tcs") is not None, "question du carnet retrouvée avec son texte depuis la banque")
    B.goto(SITE + "#carnet"); B.wait_for_selector("text=Carnet"); B.wait_for_timeout(300)
    n_before = len(base.docs)
    seance(B, 4)
    wait_sync(B, base, lambda: B.evaluate("() => Object.keys((JSON.parse(localStorage.getItem('edn-sb-sync'))||{}).dirty||{}).length") == 0 and base.clock > 0 and B.locator("text=copie en cours").count() == 0, "séance faite sur B copiée")
    locB = B.evaluate(IDB)

    print("Retour sur A : fusion")
    A.goto(SITE + "#compte"); A.click("text=Copier maintenant")
    def merged():
        la = A.evaluate(IDB)
        return all(la.get(k) == v for k, v in locB.items() if k.startswith("memoire/"))
    wait_sync(A, base, merged, "A récupère la séance faite sur B (mémoire fusionnée)")
    # Deux appareils modifient la même mémoire sans s'être synchronisés : rien ne se perd.
    ctxA.unroute(SB + "/**"); ctxA.route(SB + "/**", lambda r: r.abort())
    seance(A, 5); A.wait_for_timeout(5000)
    check(A.evaluate("() => Object.keys(JSON.parse(localStorage.getItem('edn-sb-sync')).dirty).length") > 0, "hors ligne, A garde ses changements en attente")
    seance(B, 5)
    wait_sync(B, base, lambda: B.evaluate("() => Object.keys(JSON.parse(localStorage.getItem('edn-sb-sync')).dirty).length") == 0, "B copie sa séance pendant ce temps")
    locB = B.evaluate(IDB)
    ctxA.unroute(SB + "/**"); ctxA.route(SB + "/**", base.handle)
    A.goto(SITE + "#compte"); A.click("text=Copier maintenant")
    def union():
        la = A.evaluate(IDB)
        if A.evaluate("() => Object.keys(JSON.parse(localStorage.getItem('edn-sb-sync')).dirty).length"): return False
        for k, v in locB.items():
            if not k.startswith("memoire/"): continue
            if k not in la or not set(v["q"]) <= set(la[k]["q"]) or not set(v["o"]) <= set(la[k]["o"]): return False
            if base.docs[("memoire", k[8:])]["data"] != la[k]: return False
        return True
    wait_sync(A, base, union, "A et B ont travaillé chacun de leur côté : la mémoire réunit les deux séances")
   
    B.goto(SITE + "#compte"); B.click("text=Copier maintenant")
    wait_sync(B, base, lambda: all(B.evaluate(IDB).get(k) == v for k, v in A.evaluate(IDB).items() if k.startswith("memoire/")), "B rejoint le même état")

    print("Session expirée, suppression")
    base.expire |= set(base.tokens); r0 = base.n_refresh
    A.goto(SITE + "#carnet"); A.wait_for_selector("text=Retirer du carnet >> nth=0")
    A.locator("text=Retirer du carnet").first.click()
    wait_sync(A, base, lambda: base.docs[("carnet", "banque__q" + qid2)].get("supprime") is True, "retrait du carnet transmis (jeton renouvelé au passage)")
    check(base.n_refresh > r0, "le jeton refusé a été renouvelé")
    B.goto(SITE + "#compte"); B.click("text=Copier maintenant")
    wait_sync(B, base, lambda: not any(k.startswith("carnet/") for k in B.evaluate(IDB)), "B retire aussi la question de son carnet")

    print("Déconnexion, et site sans la base")
    B.click("text=Me déconnecter"); B.wait_for_selector("text=Créer mon compte ou me connecter")
    check(B.evaluate("() => localStorage.getItem('edn-sb')") is None and any(k.startswith("memoire/") for k in B.evaluate(IDB)), "déconnecté, les données restent sur l'appareil")
    ctxC, C = device(browser, base, errors, "C")
    ctxC.unroute(SB + "/**"); ctxC.route(SB + "/**", lambda r: r.abort())
    C.goto(SITE); C.click("button:has-text('Commencer')"); seance(C)
    C.click("text=Voir la correction"); C.wait_for_selector("text=Signaler une erreur")
    check(C.locator(".tag:has-text('Non relue')").count() >= 1, "base injoignable : le site marche et affiche le niveau du fichier")
    C.goto(SITE + "#compte"); C.fill('input[type="email"]', "a@b.fr"); C.click("text=Recevoir le lien de connexion"); C.wait_for_selector("text=L'envoi a échoué")
    check(True, "base injoignable : message clair à la connexion")

    print("Dossier essai/")
    ctxE, E = device(browser, base, errors, "E")
    E.goto(SITE + "essai/"); E.click("button:has-text('Commencer')"); E.goto(SITE + "essai/#seance"); E.wait_for_selector("text=Mes items")
    check(E.locator("input.otog").count() >= 30, "essai/ lit la banque dans le dossier parent")

    check(not base.fail, "appels conformes aux droits de la base" + (" : " + " | ".join(base.fail[:5]) if base.fail else ""))
    check(not errors, "aucune erreur dans la console" + (" : " + " | ".join(errors[:5]) if errors else ""))
    browser.close()
print("%d vérifications passées" % ok)
