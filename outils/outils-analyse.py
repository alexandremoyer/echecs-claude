#!/usr/bin/env python3
"""Outils pour l'analyse des parties d'échecs (page interactive coup par coup).

Usage:
  python3 outils-analyse.py analyser PSEUDO CHOIX [--lichess]      partie en ligne: tout en une commande
  python3 outils-analyse.py analyser [PSEUDO|noirs] --pgn fichier.pgn   PGN collé par le joueur: idem
  python3 outils-analyse.py verifier partie.json SPEC...            vérifications au moteur en une commande
  python3 outils-analyse.py build partie.json analyse.json modele-analyse.html page.html
  (aussi: setup, parties PSEUDO [N], recuperer PSEUDO CHOIX, importer fichier.pgn [PSEUDO], analyse, stats, ouvertures, fiche)
Voir outils/rendu-analyse.md.
analyser = setup si besoin, puis recuperer ou importer (partie.json, avec meta: joueurs, classements, date,
cadence, couleur, résultat) et analyse (analyse.json), avec un budget de temps (BUDGET, 90 s par défaut)
pour tenir sous le délai d'une commande. Affiche: infos, pendule, analyse coup par coup (mats en clair),
indicateur de triche, étiquettes automatiques, mats manqués, ouvertures, puis le squelette des champs à
ajouter à partie.json avant build.
verifier: SPEC = COUP (position avant ce coup, ex. 9...Te8), +COUP (après), avec en option :c1,c2 pour
évaluer aussi des coups précis en français (ex. 9...Te8:exd4,Te8). Temps par position: variable T (4 s).
build: fusionne d'abord complement.json (les champs rédigés par Claude) dans partie.json s'il existe, écrit
la page (champs facultatifs complétés, syntaxe du script vérifiée avec node), puis, si
partie.json contient numero, la fiche joueur (fiche.md, d'après lecons, mots_cles, meta, analyse) et la
ligne d'index (index.txt).
Après un coup qui mate, l'évaluation vaut +100 ou -100 sans appel au moteur; après une nulle, 0.
Le moteur n'est lancé qu'une fois par position (l'éval après un coup est celle de la position suivante).
Ouvertures: base chess-openings de lichess, clonée par setup dans ~/sf/ouvertures, reconnue par position.
Parties en ligne: API publiques de chess.com (par défaut, api.chess.com doit être autorisé) et de lichess (--lichess,
ou un lien lichess comme CHOIX; lichess.org doit être autorisé). recuperer écrit partie.json avec les coups
en notation française, la pendule ([temps restant, temps du coup] en secondes) et les informations de la partie.
"""
import base64, json, os, re, shutil, subprocess, sys
HOME = os.path.expanduser("~")
SF = os.path.join(HOME, "sf", "stockfish", "stockfish-ubuntu-x86-64-avx2")
FR2EN = {"R": "K", "D": "Q", "T": "R", "F": "B", "C": "N"}
EN2FR = {"K": "R", "Q": "D", "R": "T", "B": "F", "N": "C"}
def setup():
    d = os.path.join(HOME, "sf"); os.makedirs(d, exist_ok=True)
    subprocess.run(f"pip download chess==1.10.0 --no-deps -d {d} -q && pip install --break-system-packages -q {d}/chess-1.10.0-py3-none-any.whl", shell=True, check=True)
    if not os.path.exists(SF):
        subprocess.run(f"cd {d} && curl -sSL -o sf.tar https://github.com/official-stockfish/Stockfish/releases/download/sf_17.1/stockfish-ubuntu-x86-64-avx2.tar && tar xf sf.tar && chmod +x {SF}", shell=True, check=True)
    o = os.path.join(d, "ouvertures")
    if not os.path.exists(o):
        r = subprocess.run(f"git clone -q --depth 1 https://github.com/lichess-org/chess-openings {o}", shell=True)
        if r.returncode: print("attention: base d'ouvertures non téléchargée, pas de nom d'ouverture")
    print("ok", SF)
FAMILLES = {
    "Queen's Gambit Accepted": "Gambit dame accepté", "Queen's Gambit Declined": "Gambit dame refusé", "Queen's Gambit": "Gambit dame",
    "Queen's Pawn Game": "Début du pion dame", "King's Pawn Game": "Début du pion roi", "Italian Game": "Partie italienne",
    "Ruy Lopez": "Partie espagnole", "Scotch Game": "Partie écossaise", "Vienna Game": "Partie viennoise", "Four Knights Game": "Partie des quatre cavaliers",
    "Three Knights Opening": "Partie des trois cavaliers", "Bishop's Opening": "Partie du fou", "Center Game": "Partie du centre",
    "King's Gambit Accepted": "Gambit du roi accepté", "King's Gambit Declined": "Gambit du roi refusé", "King's Gambit": "Gambit du roi",
    "Danish Gambit": "Gambit danois", "Latvian Gambit": "Gambit letton", "Elephant Gambit": "Gambit de l'éléphant", "Englund Gambit": "Gambit Englund",
    "Englund Gambit Complex": "Gambit Englund", "Blackmar-Diemer Gambit": "Gambit Blackmar-Diemer", "Petrov's Defense": "Défense Petrov",
    "Philidor Defense": "Défense Philidor", "Sicilian Defense": "Défense sicilienne", "French Defense": "Défense française",
    "Caro-Kann Defense": "Défense Caro-Kann", "Alekhine Defense": "Défense Alekhine", "Scandinavian Defense": "Défense scandinave",
    "Pirc Defense": "Défense Pirc", "Modern Defense": "Défense moderne", "Owen Defense": "Défense Owen", "Nimzowitsch Defense": "Défense Nimzowitsch",
    "Indian Defense": "Défense indienne", "King's Indian Defense": "Défense est-indienne", "Queen's Indian Defense": "Défense ouest-indienne",
    "Nimzo-Indian Defense": "Défense nimzo-indienne", "Bogo-Indian Defense": "Défense bogo-indienne", "Grünfeld Defense": "Défense Grünfeld",
    "Slav Defense": "Défense slave", "Semi-Slav Defense": "Défense semi-slave", "Dutch Defense": "Défense hollandaise", "Benoni Defense": "Défense Benoni",
    "Benko Gambit": "Gambit Benko", "Budapest Defense": "Gambit de Budapest", "London System": "Système de Londres", "English Opening": "Ouverture anglaise",
    "Réti Opening": "Ouverture Réti", "Zukertort Opening": "Ouverture Zukertort", "Bird Opening": "Ouverture Bird", "Nimzo-Larsen Attack": "Attaque Nimzo-Larsen",
    "Polish Opening": "Ouverture polonaise", "Polish Defense": "Défense polonaise", "Grob Opening": "Ouverture Grob", "Saragossa Opening": "Ouverture Saragosse", "Mieses Opening": "Ouverture Mieses",
    "Van't Kruijs Opening": "Ouverture Van't Kruijs", "Amar Opening": "Ouverture Amar", "Ware Opening": "Ouverture Ware", "Sodium Attack": "Attaque Sodium",
}
MOTS = {"Advance": "d'avance", "Exchange": "d'échange", "Classical": "classique", "Modern": "moderne", "Normal": "normale",
        "Closed": "fermée", "Open": "ouverte", "Accelerated": "accélérée", "Main": "principale", "Fianchetto": "fianchetto"}
def nom_fr(name):
    """Nom de la base lichess en français: famille traduite, 'X Variation' devient 'variante X'."""
    fam, _, reste = name.partition(": ")
    out = [FAMILLES.get(fam, fam)]
    for v in [x for x in reste.split(", ") if x]:
        if v.endswith(" Variation"):
            v = "variante " + " ".join(MOTS.get(w, w) for w in v[:-10].split())
        elif v == "Main Line": v = "ligne principale"
        out.append(v)
    return ", ".join(out)
def ouvertures(mv_list):
    """Pour chaque demi-coup: ouverture reconnue par position (base lichess), ordre de coups inhabituel,
    ou sortie de la théorie. None quand il n'y a rien à dire ou que la base est absente."""
    import chess, csv, glob
    book = {}
    for f in sorted(glob.glob(os.path.join(HOME, "sf", "ouvertures", "?.tsv"))):
        for row in csv.DictReader(open(f), delimiter="\t"):
            bb = chess.Board()
            for tok in row["pgn"].split():
                if not tok[0].isdigit(): bb.push_san(tok)
            book[bb.epd()] = (row["eco"], row["name"])
    if not book: return [None] * len(mv_list)
    b = chess.Board(); names = []
    for m in mv_list:
        b.push(b.parse_san(fr2en(m))); names.append(book.get(b.epd()))
    last = max([i for i, n in enumerate(names) if n], default=-1); cur = None; out = []
    for i, n in enumerate(names):
        if n: cur = n; out.append(f"Théorie: {nom_fr(n[1])} ({n[0]})")
        elif i < last and cur: out.append(f"Théorie: ordre de coups inhabituel ({nom_fr(cur[1])}), la théorie reprend ensuite")
        elif i == last + 1 and cur: out.append(f"Sortie de la théorie. Dernière position connue: {nom_fr(cur[1])} ({cur[0]})")
        else: out.append(None)
    return out
def afficher_ouvertures(mv_list):
    print("Ouvertures (base lichess):")
    for lab, o in zip(labels(mv_list), ouvertures(mv_list)):
        if o: print(f"- {lab}: {o}")
UA = "echecs-claude (github.com/alexandremoyer/echecs-claude)"
def api(url, ndjson=False):
    cmd = ["curl", "-sS", "-f", "-m", "60", "-A", UA] + (["-H", "Accept: application/x-ndjson"] if ndjson else []) + [url]
    r = subprocess.run(cmd, capture_output=True, text=True); dom = url.split("/")[2]
    if r.returncode:
        sys.exit(f"{dom} inaccessible ({r.stderr.strip()[:150]}). Autoriser {dom} dans les domaines autorisés de claude.ai, ou demander le PGN au joueur.")
    return [json.loads(l) for l in r.stdout.splitlines() if l.strip()] if ndjson else json.loads(r.stdout)
def parties_chesscom(pseudo, n):
    arch = api(f"https://api.chess.com/pub/player/{pseudo.lower()}/games/archives")["archives"]; out = []
    for u in reversed(arch):
        out += sorted(api(u)["games"], key=lambda g: g["end_time"], reverse=True)
        if len(out) >= n: break
    return out[:n]
LI_FIN = {"mate": "checkmated", "resign": "resigned", "outoftime": "timeout", "timeout": "abandoned"}
def parties_lichess(pseudo, n):
    """Parties lichess converties au format des parties chess.com (champs utilisés par ligne_partie et recuperer)."""
    out = []
    for g in api(f"https://lichess.org/api/games/user/{pseudo}?max={n}&clocks=true&opening=true&pgnInJson=true", ndjson=True):
        st, win, ck = g.get("status"), g.get("winner"), g.get("clock")
        x = {"pgn": g.get("pgn", ""), "url": "https://lichess.org/" + g["id"], "end_time": g.get("lastMoveAt", g.get("createdAt", 0)) // 1000,
             "time_class": g.get("speed"), "time_control": f"{ck['initial']}+{ck['increment']}" if ck else "-", "eco": g.get("opening", {}).get("name", "")}
        for c in ("white", "black"):
            pl = g["players"][c]
            res = "win" if win == c else (LI_FIN.get(st, st) if win else st)
            x[c] = {"username": pl.get("user", {}).get("name", "anonyme"), "rating": pl.get("rating", "?"), "result": res}
        out.append(x)
    return out
def parties_en_ligne(pseudo, n, lichess=False): return parties_lichess(pseudo, n) if lichess else parties_chesscom(pseudo, n)
FIN = {"checkmated": "par mat", "resigned": "par abandon", "timeout": "au temps", "abandoned": "par abandon (déconnexion)"}
NUL = {"agreed": "d'un commun accord", "repetition": "par répétition", "stalemate": "par pat", "insufficient": "par matériel insuffisant",
       "50move": "par la règle des 50 coups", "timevsinsufficient": "temps contre matériel insuffisant", "draw": ""}
def resultat(g, pseudo):
    moi = "white" if g["white"]["username"].lower() == pseudo.lower() else "black"; adv = "black" if moi == "white" else "white"
    r, ra = g[moi]["result"], g[adv]["result"]
    if r == "win": return moi, adv, ("victoire " + FIN.get(ra, "")).strip()
    if r in ("aborted", "noStart"): return moi, adv, "partie annulée"
    if r in NUL: return moi, adv, ("nulle " + NUL[r]).strip()
    return moi, adv, ("défaite " + FIN.get(r, "")).strip()
def ligne_partie(i, g, pseudo):
    from datetime import datetime
    from zoneinfo import ZoneInfo
    d = datetime.fromtimestamp(g["end_time"], ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M")
    moi, adv, res = resultat(g, pseudo); nb = max([int(x) for x in re.findall(r"(\d+)\. ", g.get("pgn", ""))] or [0])
    ouv = g.get("eco", "").rsplit("/", 1)[-1].replace("-", " ")
    return f"{i}. {d} | {g.get('time_class')} {g.get('time_control')} | {'Blancs' if moi == 'white' else 'Noirs'} contre {g[adv]['username']} ({g[adv]['rating']}) | {res} | {nb} coups | {ouv}"
def lister(pseudo, n=10, lichess=False):
    for i, g in enumerate(parties_en_ligne(pseudo, n, lichess), 1): print(ligne_partie(i, g, pseudo))
def mmss(s): s = int(round(s)); return f"{s // 60}:{s % 60:02d}"
def duree(s): return f"{s:.0f} s" if s < 60 else mmss(s)
def recuperer(pseudo, choix, out="partie.json", lichess=False):
    import chess.pgn, io
    lichess = lichess or "lichess.org" in choix; games = parties_en_ligne(pseudo, 300, lichess)
    if choix.isdigit() and len(choix) < 5: g = games[int(choix) - 1]
    else:
        c = re.sub(r"/(white|black)$", "", choix.lower().rstrip("/")); cid = c.split("/")[-1]
        cands = [x for x in games if x["url"].lower().rstrip("/").endswith("/" + cid) or c in (x["white"]["username"].lower(), x["black"]["username"].lower())]
        if not cands: sys.exit(f"partie introuvable parmi les {len(games)} dernières: {choix}")
        g = cands[0]
    moi, adv, res = resultat(g, pseudo)
    p = partie_depuis_pgn(g["pgn"], moi == "black", "lichess" if lichess else "chess.com", res, g["url"])
    json.dump(p, open(out, "w"), ensure_ascii=False, indent=1)
    print(p["infos"]); print(p["coups"])
    if p["pendule"]: resume_pendule(moves_of(p["coups"]), p["pendule"])
def cadence_txt(tc):
    """'600' -> '10 min', '600+5' -> '10 min + 5 s', '180' -> '3 min', sinon tel quel."""
    m = re.match(r"^(\d+)(?:\+(\d+))?$", tc or "")
    if not m: return tc or "?"
    s = int(m.group(1)); base = f"{s // 60} min" if s % 60 == 0 else f"{s} s"
    return base + (f" + {m.group(2)} s" if m.group(2) and m.group(2) != "0" else "")
def date_fr(d):
    m = re.match(r"(\d{4})[./-](\d\d)[./-](\d\d)", d or "")
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else (d or "?")
def partie_depuis_pgn(pgn, noirs, plateforme, res=None, url=""):
    """partie.json (coups en français, flip, pendule, infos, meta) à partir d'un PGN (texte)."""
    import chess.pgn, io
    game = chess.pgn.read_game(io.StringIO(pgn)); h = game.headers; tc = h.get("TimeControl", "-")
    base, inc = (tc.split("+") + ["0"])[:2] if tc[:1].isdigit() and "/" not in tc else (None, "0")
    b = game.board(); toks, pend = [], []; last = [float(base)] * 2 if base else None
    for node in game.mainline():
        side = 0 if b.turn else 1; san = en2fr(b.san(node.move))
        toks.append(f"{b.fullmove_number}.{san}" if b.turn else san); b.push(node.move); c = node.clock()
        if c is not None and last: pend.append([round(c, 1), round(max(0, last[side] - c + float(inc)), 1)]); last[side] = c
        else: pend.append(None)
    if res is None:
        r = h.get("Result", "*"); gagne = {"1-0": not noirs, "0-1": noirs}.get(r)
        fin = "par mat" if b.is_checkmate() else ("par pat" if b.is_stalemate() else "")
        res = ("nulle " + fin) if r == "1/2-1/2" else ("victoire " + fin) if gagne else ("défaite " + fin) if gagne is False else "résultat inconnu"
        res = res.strip()
    nb = (len(toks) + 1) // 2
    meta = {"plateforme": plateforme, "blancs": h.get("White", "?"), "elo_blancs": h.get("WhiteElo", "?"), "noirs": h.get("Black", "?"), "elo_noirs": h.get("BlackElo", "?"),
            "date": date_fr(h.get("Date")), "cadence": cadence_txt(tc), "couleur": "Noirs" if noirs else "Blancs", "resultat": res, "nb_coups": nb, "url": url}
    infos = (f"{plateforme}: {meta['blancs']} ({meta['elo_blancs']}) contre {meta['noirs']} ({meta['elo_noirs']}), {meta['date']}, cadence {meta['cadence']}, "
             f"joueur avec les {meta['couleur']}, {res} au {nb}e coup. " + (h.get('Termination', '') + ". " if h.get('Termination') not in (None, '', 'Normal', '*') else "") + url).strip()
    return {"coups": " ".join(toks), "flip": noirs, "pendule": pend if any(pend) else None, "infos": infos, "meta": meta}
def importer_pgn(path, pseudo=None, out="partie.json"):
    """PGN collé par le joueur: écrit partie.json. Le pseudo (ou 'noirs') donne la couleur du joueur; sinon Blancs."""
    import chess.pgn, io
    txt = open(path).read(); h = chess.pgn.read_game(io.StringIO(txt)).headers
    noirs = (pseudo or "").lower() in ("noirs", "noir", "black") or (pseudo is not None and h.get("Black", "").lower() == pseudo.lower())
    plateforme = "avec Claude" if "claude" in (h.get("White", "") + h.get("Black", "")).lower() else {"chess.com": "chess.com", "lichess": "lichess"}.get(h.get("Site", "").lower().replace("https://", "").split("/")[0].replace("www.", ""), h.get("Site", "PGN") or "PGN")
    p = partie_depuis_pgn(txt, noirs, plateforme, url=h.get("Link", ""))
    json.dump(p, open(out, "w"), ensure_ascii=False, indent=1); print(p["infos"]); print(p["coups"])
    if p["pendule"]: resume_pendule(moves_of(p["coups"]), p["pendule"])
def resume_pendule(mv_list, pend):
    print("Pendule:"); labs = labels(mv_list)
    for side, name in ((0, "Blancs"), (1, "Noirs")):
        pts = [(labs[i], q) for i, q in enumerate(pend) if q and i % 2 == side]
        if not pts: continue
        rapides = sum(1 for _, q in pts if q[1] < 3); longs = sorted(pts, key=lambda x: -x[1][1])[:3]
        print(f"- {name}: temps utilisé {mmss(sum(q[1] for _, q in pts))}, reste {mmss(pts[-1][1][0])} à la fin, {rapides} coups sur {len(pts)} joués en moins de 3 s, plus longues réflexions: "
              + ", ".join(f"{l} ({duree(q[1])})" for l, q in longs))
def fr2en(san):
    san = re.sub(r"=([DTFC])", lambda m: "=" + FR2EN[m.group(1)], san)
    return FR2EN[san[0]] + san[1:] if san[0] in FR2EN else san
def en2fr(san):
    """Coup en notation anglaise vers le français; accepte un préfixe de numéro (15.Nf3, 15...Nf6)."""
    pre, san = re.match(r"^(\d+\.(?:\.\.)?)?(.*)$", san).groups()
    san = re.sub(r"=([QRBN])", lambda m: "=" + EN2FR[m.group(1)], san)
    return (pre or "") + (EN2FR[san[0]] + san[1:] if san and san[0] in EN2FR else san)
def moves_of(txt):
    toks = [t for t in re.sub(r"\d+\.(\.\.)?", " ", txt).split() if t not in ("1-0", "0-1", "1/2-1/2", "*")]
    return [t.rstrip("!?") for t in toks]
def analyse(pj, out):
    import chess, chess.engine
    p = json.load(open(pj)); b = chess.Board(); eng = chess.engine.SimpleEngine.popen_uci(SF)
    res = []
    def sc(x): return x["score"].white().score(mate_score=10000)
    D = int(os.environ.get("DEPTH", "20")); mv_list = moves_of(p["coups"])
    eng.configure({"Threads": os.cpu_count() or 1, "Hash": 128})
    T = float(os.environ.get("BUDGET", "90")) / (len(mv_list) + 1)
    def top(bd): return eng.analyse(bd, chess.engine.Limit(depth=D, time=T), multipv=3)
    info = top(b); labs = labels(mv_list)
    for k, m in enumerate(mv_list):
        best = [[en2fr(b.san(x["pv"][0])), sc(x) / 100, " ".join(en2fr(s) for s in b.variation_san(x["pv"][:6]).split()), x["score"].white().mate()] for x in info]
        mv = b.parse_san(fr2en(m)); fen = b.fen(); b.push(mv)
        if b.is_checkmate(): after = 10000 if b.turn == chess.BLACK else -10000; mate = 0
        elif b.is_game_over(): after = 0; mate = None
        else: info = top(b); after = sc(info[0]); mate = info[0]["score"].white().mate()
        res.append(dict(ply=k, san=m, fen_before=fen, after=after / 100, best=best, mate=mate))
        print(f"{labs[k]} après {texte_eval(after / 100, mate)} | meilleurs: " + " / ".join(f"{s} ({texte_eval(e, mt)}) {pv}" for s, e, pv, mt in best), flush=True)
    eng.quit(); json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
    stats(out, pj); afficher_ouvertures(moves_of(p["coups"]))
def texte_eval(e, mate=None):
    """Evaluation lisible: '+1.2', ou 'mat en 3 pour les Blancs' (mat=0: mat sur l'échiquier)."""
    if mate is None: return f"{e:+.2f}"
    if mate == 0: return "mat"
    return f"mat en {abs(mate)} pour les {'Blancs' if mate > 0 else 'Noirs'}"
def position_avant(mv_list, spec):
    """Position désignée par un coup de la partie en français ('9...Te8': avant ce coup; '+9...Te8': après)."""
    import chess
    apres = spec.startswith("+"); key = norm(spec.lstrip("+")); b = chess.Board()
    for lab, m in zip(labels(mv_list), mv_list):
        if norm(lab) == key:
            if apres: b.push(b.parse_san(fr2en(m)))
            return b, ("après " if apres else "avant ") + lab
        b.push(b.parse_san(fr2en(m)))
    sys.exit(f"coup inconnu dans la partie: {spec}")
def verifier(pj, specs):
    """Vérifications au moteur en une commande. Chaque spec: COUP (position avant ce coup), +COUP (après),
    avec en option :c1,c2 pour évaluer aussi des coups précis (notation française). Ex: 9...Te8:exd4,Te8 +14.Fd2"""
    import chess, chess.engine, time
    p = json.load(open(pj)); mv_list = moves_of(p["coups"]); eng = chess.engine.SimpleEngine.popen_uci(SF)
    eng.configure({"Threads": os.cpu_count() or 1, "Hash": 128})
    T = min(float(os.environ.get("T", "4")), float(os.environ.get("BUDGET", "90")) / max(1, len(specs) * 2))
    def ligne(x, bd): return f"  {texte_eval(sc(x) / 100, x['score'].white().mate())}: " + " ".join(en2fr(s) for s in bd.variation_san(x["pv"][:10]).split())
    def sc(x): return x["score"].white().score(mate_score=10000)
    for spec in specs:
        pos, _, cands = spec.partition(":"); bd, lab = position_avant(mv_list, pos)
        print(f"== {lab}, trait aux {'Blancs' if bd.turn else 'Noirs'}" + (", mat sur l'échiquier" if bd.is_checkmate() else ""), flush=True)
        if bd.is_game_over(): continue
        for x in eng.analyse(bd, chess.engine.Limit(time=T), multipv=3): print(ligne(x, bd), flush=True)
        for c in [c for c in cands.split(",") if c]:
            try: mv = bd.parse_san(fr2en(c))
            except Exception: print(f"  {c}: coup illégal ici"); continue
            x = eng.analyse(bd, chess.engine.Limit(time=T), root_moves=[mv]); print(f"  {c} seulement ->" + ligne(x, bd)[1:], flush=True)
    eng.quit()
def stats(aj, pj=None):
    """Indicateur de triche: perte moyenne par coup (plafonnée à 10 points), coups au niveau
    du moteur, erreurs de plus d'un point, pour chaque camp, à partir du 3e coup."""
    an = json.load(open(aj)); print("Indicateur de triche (à partir du 3e coup):")
    pend = (json.load(open(pj)).get("pendule") if pj else None) or []
    for side, name in ((0, "Blancs"), (1, "Noirs")):
        losses, top, errs = [], 0, []
        for a in an:
            if a["ply"] % 2 != side or a["ply"] < 4 or not a["best"]: continue
            l = a["best"][0][1] - a["after"]
            l = max(0, min(10, l if side == 0 else -l)); losses.append(l)
            if a["san"].rstrip("+#") == a["best"][0][0].rstrip("+#") or l <= 0.1: top += 1
            if l > 1:
                t = pend[a["ply"]] if a["ply"] < len(pend) and pend[a["ply"]] else None
                errs.append(f"{a['ply'] // 2 + 1}{'.' if side == 0 else '...'}{a['san']} ({l:.1f}{', joué en ' + duree(t[1]) if t else ''})")
        if not losses: continue
        print(f"- {name}: {round(100 * sum(losses) / len(losses))} centièmes par coup, {top} coups sur {len(losses)} au niveau du moteur, {len(errs)} erreurs de plus d'un point: {', '.join(errs) or 'aucune'}")
    tags = [f"{a['ply'] // 2 + 1}{'.' if a['ply'] % 2 == 0 else '...'}{a['san']} {auto_tag(a)}" for a in an if auto_tag(a) != "bon"]
    print("Etiquettes automatiques (coups qui ne sont pas notés bon):", ", ".join(tags) or "aucune")
    mm = mats_manques(an)
    if mm: print("Mats manqués (mat forcé disponible, coup joué sans mat forcé):", ", ".join(mm))
def mats_manques(an):
    out = []
    for a in an:
        if not a["best"] or len(a["best"][0]) < 4: continue
        s = 1 if a["ply"] % 2 == 0 else -1; m = a["best"][0][3]; m2 = a.get("mate")
        if m is None or m * s <= 0: continue
        garde = m2 is not None and (m2 == 0 or m2 * s > 0)
        if garde and abs(m2) <= abs(m): continue
        out.append(f"{a['ply'] // 2 + 1}{'.' if s == 1 else '...'}{a['san']} (mat en {abs(m)} par {a['best'][0][0]}" + (f", il reste un mat en {abs(m2)}" if garde else "") + ")")
    return out
def resume_indicateur(an, pend):
    """Une phrase par camp pour la fiche: perte moyenne, coups au niveau du moteur, erreurs."""
    out = []
    for side, name in ((0, "Blancs"), (1, "Noirs")):
        losses, top, errs = [], 0, 0
        for a in an:
            if a["ply"] % 2 != side or a["ply"] < 4 or not a["best"]: continue
            l = a["best"][0][1] - a["after"]; l = max(0, min(10, l if side == 0 else -l)); losses.append(l)
            if a["san"].rstrip("+#") == a["best"][0][0].rstrip("+#") or l <= 0.1: top += 1
            if l > 1: errs += 1
        if losses: out.append(f"{name} {round(100 * sum(losses) / len(losses))} centièmes par coup, {top} coups sur {len(losses)} au niveau du moteur, {errs} erreurs de plus d'un point")
    return "; ".join(out)
def resume_pendule_court(mv_list, pend):
    out = []
    for side, name in ((0, "Blancs"), (1, "Noirs")):
        pts = [q for i, q in enumerate(pend) if q and i % 2 == side]
        if pts: out.append(f"{name} {mmss(sum(q[1] for q in pts))} utilisées, {mmss(pts[-1][0])} restantes, {sum(1 for q in pts if q[1] < 3)} coups sur {len(pts)} en moins de 3 s")
    return "; ".join(out)
def ouverture_nom(mv_list):
    noms = [o for o in ouvertures(mv_list) if o and o.startswith("Théorie: ") and "inhabituel" not in o]
    return noms[-1][9:].rsplit(" (", 1)[0] if noms else "ouverture non reconnue"
def fiche(p, an, out_fiche="fiche.md", out_index="index.txt"):
    """Fiche joueur/parties/partie-NNN.md et ligne d'index, d'après partie.json (numero, titre, lecons, mots_cles, meta) et analyse.json."""
    mv_list = moves_of(p["coups"]); m = p.get("meta") or {}; n = p["numero"]
    couleur = m.get("couleur") or ("Noirs" if p.get("flip") else "Blancs"); plat = m.get("plateforme", "?"); date = m.get("date", "?")
    res = f"{m.get('resultat', 'résultat inconnu')} au {m.get('nb_coups', (len(mv_list) + 1) // 2)}e coup"; ouv = ouverture_nom(mv_list)
    titre = p.get("titre") or "aucune"; pend = p.get("pendule") or []
    lignes = [f"# Partie {n} ({date}), {plat}, avec les {couleur}, {ouv}, {res}",
              f"{m.get('blancs', 'Blancs')} ({m.get('elo_blancs', '?')}) contre {m.get('noirs', 'Noirs')} ({m.get('elo_noirs', '?')}), cadence {m.get('cadence', '?')}. Analyse: \"{titre}\".",
              p["coups"], "", "Leçons:"] + [f"- {l}" for l in p.get("lecons", [])]
    if pend: lignes.append(f"- Pendule: {resume_pendule_court(mv_list, pend)}.")
    lignes.append(f"- Indicateur de triche (information, pas un verdict): {resume_indicateur(an, pend)}.")
    mm = mats_manques(an)
    if mm: lignes.append(f"- Mats manqués: {', '.join(mm)}.")
    open(out_fiche, "w").write("\n".join(lignes) + "\n")
    mots = p.get("mots_cles") or [ouv]
    ligne = f"| {n} | {date} | {plat}, {couleur}, {res} | {'; '.join(mots)} | {titre} |"
    open(out_index, "w").write(ligne + "\n")
    print(f"fiche: {out_fiche} (a écrire dans joueur/parties/partie-{n:03d}.md par local_path)"); print("ligne d'index:", ligne)
def clair(b, mv):
    import chess
    NAME = {chess.PAWN: ("pion", "m"), chess.KNIGHT: ("cavalier", "m"), chess.BISHOP: ("fou", "m"),
            chess.ROOK: ("tour", "f"), chess.QUEEN: ("dame", "f"), chess.KING: ("roi", "m")}
    p = b.piece_at(mv.from_square); n, g = NAME[p.piece_type]
    col = ("blanche" if p.color else "noire") if g == "f" else ("blanc" if p.color else "noir")
    art = "La" if g == "f" else "Le"; s = b.san(mv)
    if b.is_castling(mv):
        t = ("Les Blancs" if p.color else "Les Noirs") + (" font le petit roque" if chess.square_file(mv.to_square) == 6 else " font le grand roque")
    elif b.is_capture(mv):
        c = b.piece_at(mv.to_square)
        if c is None:
            t = f"{art} {n} {col} {chess.square_name(mv.from_square)} prend le pion en passant en {chess.square_name(mv.to_square)}"
        else:
            cn, cg = NAME[c.piece_type]
            t = f"{art} {n} {col} {chess.square_name(mv.from_square)} prend {'la' if cg == 'f' else 'le'} {cn} en {chess.square_name(mv.to_square)}"
    else:
        t = f"{art} {n} {col} {chess.square_name(mv.from_square)} va en {chess.square_name(mv.to_square)}"
    if mv.promotion:
        t += ", promotion en " + NAME[mv.promotion][0]
    if s.endswith("#"): t += ", échec et mat"
    elif s.endswith("+"): t += ", avec échec"
    return t + "."
def pieces_js():
    import chess.svg
    out = {}
    for sym in "PNBRQKpnbrqk":
        g = chess.svg.PIECES[sym]
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="45" height="45">' + g + "</svg>"
        out[sym] = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    return json.dumps(out)
def auto_tag(a):
    """Etiquette d'après la perte mesurée par le moteur (voir regles/analyse.md)."""
    if not a["best"]: return "bon"
    s = 1 if a["ply"] % 2 == 0 else -1
    before = max(-10, min(10, s * a["best"][0][1])); after = max(-10, min(10, s * a["after"]))
    loss = max(0, before - after)
    if loss <= 0.5: return "bon"
    if after >= 5 or (before <= -5 and loss <= 2.5): return "imprecis"
    if loss <= 1 or (loss <= 2.5 and abs(after) < 1): return "imprecis"
    if loss <= 2.5: return "erreur"
    return "erreur" if after >= 1.5 else "gaffe"
def labels(mv_list):
    import chess
    b = chess.Board(); out = []
    for m in mv_list:
        mv = b.parse_san(fr2en(m)); out.append(f"{b.fullmove_number}{'.' if b.turn else '...'}{en2fr(b.san(mv))}"); b.push(mv)
    return out
def norm(lab): return re.sub(r"[+#!?\s]", "", lab)
def commentaires(p, mv_list):
    """Commentaires: dictionnaire {coup en notation française: commentaire}, ou ancienne liste complète."""
    c = p.get("commentaires", {})
    if isinstance(c, list):
        assert len(c) == len(mv_list), "liste de commentaires: un par demi-coup"
        return dict(enumerate(c))
    idx = {norm(l): i for i, l in enumerate(labels(mv_list))}
    out = {}
    for k, v in c.items():
        assert norm(k) in idx, f"commentaire sur un coup qui n'est pas dans la partie: {k}"
        out[idx[norm(k)]] = v
    return out
def build(pj, aj, tpl, out):
    import chess
    p = json.load(open(pj)); an = json.load(open(aj)); mv_list = moves_of(p["coups"])
    comp = os.path.join(os.path.dirname(pj) or ".", "complement.json")
    if os.path.exists(comp):
        p.update(json.load(open(comp))); json.dump(p, open(pj, "w"), ensure_ascii=False, indent=1); print("complement.json fusionné dans", pj)
    for k, v in {"titre": "Analyse de la partie", "flip": False, "depart": "Position de départ.", "entete": "", "remarques": "", "bilan": "", "variantes": [], "commentaires": {}}.items():
        if p.get(k) is None: p[k] = v
    assert len(mv_list) == len(an), "analyse.json ne correspond pas aux coups"
    com = commentaires(p, mv_list); ops = ouvertures(mv_list); pend = p.get("pendule") or []
    b = chess.Board(); PL = [{"fen": b.board_fen(), "eval": 0.3, "mate": None}]; befores = []
    for k, m in enumerate(mv_list):
        c = com.get(k, {}); mv = b.parse_san(fr2en(m)); before = b.board_fen(); befores.append(b.fen())
        bsan = c.get("best") or an[k]["best"][0][0]; bm = b.parse_san(fr2en(bsan))
        cl = clair(b, mv); san = en2fr(b.san(mv)); b.push(mv)
        ev = an[k]["after"]; ev = max(-100, min(100, ev))
        PL.append({"num": k // 2 + 1, "side": "B" if k % 2 == 0 else "N", "san": san, "clair": cl,
                   "fen": b.board_fen(), "before": before, "frm": mv.uci()[:2], "to": mv.uci()[2:4],
                   "eval": round(ev, 1), "mate": None, "opening": ops[k], "clock": f"Pendule: coup joué en {duree(pend[k][1])}, reste {mmss(pend[k][0])}" if k < len(pend) and pend[k] else None, "tag": c.get("tag") or auto_tag(an[k]), "text": c.get("text", ""),
                   "best": {"san": en2fr(chess.Board(befores[-1]).san(bm)), "frm": bm.uci()[:2], "to": bm.uci()[2:4], "played": bm == mv},
                   "arrows": [{"kind": "threat", "frm": a, "to": z} for a, z in c.get("rouge", [])]})
    befores.append(b.fen())
    V = []
    for v in p.get("variantes", []):
        bb = chess.Board(befores[v["avant"]]); red = v.get("rouge", {})
        steps = [{"lab": "Position", "fen": bb.board_fen(), "hl": [], "red": red.get("0", []), "note": v["notes"][0]}]
        for i, s in enumerate(v["coups"]):
            mv = bb.parse_san(fr2en(s)); lab = f"{bb.fullmove_number}{'.' if bb.turn else '...'}{en2fr(bb.san(mv))}"; bb.push(mv)
            steps.append({"lab": lab, "fen": bb.board_fen(), "hl": [mv.uci()[:2], mv.uci()[2:4]], "red": red.get(str(i + 1), []), "note": v["notes"][i + 1]})
        V.append({"name": v["nom"], "steps": steps})
    h = open(tpl).read()
    for k, val in {"{{TITRE}}": p["titre"], "{{ENTETE}}": p["entete"], "{{REMARQUES}}": p["remarques"], "{{BILAN}}": p["bilan"]}.items():
        h = h.replace(k, val)
    h = h.replace("__PLIES__", json.dumps(PL, ensure_ascii=False)).replace("__VARS__", json.dumps(V, ensure_ascii=False))
    h = h.replace("__FLIP__", "true" if p["flip"] else "false").replace("__DEPART__", json.dumps(p["depart"], ensure_ascii=False))
    if "__PIECES__" in h: h = h.replace("__PIECES__", pieces_js())
    open(out, "w").write(h); check_js(h); print("ok", out, len(h))
    if p.get("numero"): fiche(p, an)
    else: print("pas de numero dans partie.json: fiche et ligne d'index non générées")
def squelette(p):
    """Ce que Claude ajoute à partie.json avant build (affiché à la fin de analyser)."""
    m = p.get("meta") or {}; j = "Noirs" if p.get("flip") else "Blancs"; a = "Blancs" if j == "Noirs" else "Noirs"
    ex = {"numero": "<dernier numéro de l'index + 1, archives comprises>", "titre": "<thème clé, 2 à 4 mots>",
          "entete": f"<div class='eyebrow'><span>{m.get('plateforme', 'plateforme')}, {m.get('date', 'JJ/MM/AAAA')}</span><span>Avec les {j}</span></div>\n<h1><titre></h1>\n<p class='players'><strong>{m.get('blancs', 'Blancs')}</strong> (Blancs, {m.get('elo_blancs', '?')}) contre <strong>{m.get('noirs', 'Noirs')}</strong> (Noirs, {m.get('elo_noirs', '?')}). <ouverture>, <span class='mono'><premiers coups></span>. <résultat> <span class='result'><mot clé du résultat></span></p>",
          "commentaires": {"<coup, ex. 9...Te8>": {"text": "<commentaire>", "tag": "<facultatif: excellent, bon, imprecis, erreur, gaffe>", "best": "<facultatif, coup en français>", "rouge": [["<case>", "<case>"]]}},
          "remarques": "<facultatif, HTML: réponses aux remarques du joueur>",
          "bilan": "<div class='cols'><div class='card'><h3>Points positifs</h3><ul><li>...</li></ul></div><div class='card'><h3>A retenir</h3><ul><li>...</li></ul></div></div>\n<p class='key'><b>Leçon clé.</b> ...</p>",
          "lecons": ["<coup, symbole, explication courte et meilleure alternative>", "Remarque du joueur: \"...\". <réponse>", "Points positifs: ..."],
          "mots_cles": ["<ouverture>", "<4 ou 5 thèmes, sans coups ni chiffres>"]}
    print("\nA écrire dans complement.json (fusionné dans partie.json par build). Ne commenter que les coups qui comptent (une douzaine au plus):")
    print("{\n" + ",\n".join(f" {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in ex.items()) + "\n}")
    print("Commande suivante, en une seule étape: cat > complement.json <<'EOF' ... EOF && python3 outils-analyse.py build partie.json analyse.json modele-analyse.html page.html")
def analyser(pseudo, choix, lichess=False, pgn=None):
    import time; t0 = time.time()
    if not os.path.exists(SF): setup()
    if "BUDGET" not in os.environ: os.environ["BUDGET"] = str(max(30, 95 - (time.time() - t0)))
    if pgn: importer_pgn(pgn, pseudo, "partie.json")
    else: recuperer(pseudo, choix, "partie.json", lichess)
    analyse("partie.json", "analyse.json"); squelette(json.load(open("partie.json")))
def check_js(h):
    node = shutil.which("node")
    if not node: print("attention: node absent, syntaxe du script non vérifiée"); return
    js = h[h.rindex("<script>") + 8:h.rindex("</script>")]
    r = subprocess.run([node, "-e", "new Function(require('fs').readFileSync(0, 'utf8'))"], input=js, text=True, capture_output=True)
    if r.returncode:
        msg = [l for l in r.stderr.splitlines() if l.strip() and len(l) < 200][:4]
        sys.exit("erreur de syntaxe dans le script de la page: " + " | ".join(msg))
    print("script de la page: syntaxe ok")
if __name__ == "__main__":
    a = sys.argv[1:]; LI = "--lichess" in a; a = [x for x in a if x != "--lichess"]
    PGN = a[a.index("--pgn") + 1] if "--pgn" in a else None
    if PGN: a = [x for x in a if x not in ("--pgn", PGN)]
    {"analyser": lambda: analyser(a[1] if len(a) > 1 else None, a[2] if len(a) > 2 else None, LI, PGN), "setup": lambda: setup(), "analyse": lambda: analyse(*a[1:3]),
     "stats": lambda: stats(a[1], a[2] if len(a) > 2 else None), "parties": lambda: lister(a[1], int(a[2]) if len(a) > 2 else 10, LI),
     "recuperer": lambda: recuperer(a[1], a[2], a[3] if len(a) > 3 else "partie.json", LI), "importer": lambda: importer_pgn(PGN or a[1], a[2] if len(a) > 2 else None),
     "verifier": lambda: verifier(a[1], a[2:]), "ouvertures": lambda: afficher_ouvertures(moves_of(json.load(open(a[1]))["coups"])),
     "build": lambda: build(*a[1:5]), "fiche": lambda: fiche(json.load(open(a[1])), json.load(open(a[2])))}[a[0]]()
