#!/usr/bin/env python3
"""Outils pour l'analyse des parties d'échecs (page interactive coup par coup).

Usage:
  python3 outils-analyse.py setup
  python3 outils-analyse.py analyse partie.json analyse.json
  python3 outils-analyse.py stats analyse.json [partie.json]
  python3 outils-analyse.py parties PSEUDO [N] [--lichess]
  python3 outils-analyse.py recuperer PSEUDO CHOIX [partie.json] [--lichess]
  python3 outils-analyse.py build partie.json analyse.json modele-analyse.html sortie.html
Voir outils/rendu-analyse.md. Si le modèle contient __PIECES__, les pièces cburnett sont
générées depuis chess.svg (python-chess) au lieu d'être recopiées en base64.
Après un coup qui mate, l'évaluation vaut +100 ou -100 sans appel au moteur; après une
nulle (pat, répétition), elle vaut 0. La traduction en clair signale les promotions.
La commande analyse affiche à la fin l'indicateur de triche (aussi disponible par stats).
La commande build vérifie elle-même la syntaxe du script de la page avec node.
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
    game = chess.pgn.read_game(io.StringIO(g["pgn"])); tc = game.headers.get("TimeControl", "-")
    base, inc = (tc.split("+") + ["0"])[:2] if tc[:1].isdigit() and "/" not in tc else (None, "0")
    b = game.board(); toks, pend = [], []; last = [float(base)] * 2 if base else None
    for node in game.mainline():
        side = 0 if b.turn else 1; san = en2fr(b.san(node.move))
        toks.append(f"{b.fullmove_number}.{san}" if b.turn else san); b.push(node.move); c = node.clock()
        if c is not None and last: pend.append([round(c, 1), round(max(0, last[side] - c + float(inc)), 1)]); last[side] = c
        else: pend.append(None)
    moi, adv, res = resultat(g, pseudo); h = game.headers
    infos = (f"{'lichess' if lichess else 'chess.com'}: {h.get('White')} ({h.get('WhiteElo')}) contre {h.get('Black')} ({h.get('BlackElo')}), {h.get('Date', '').replace('.', '/')}, "
             f"cadence {tc}, {pseudo} avec les {'Blancs' if moi == 'white' else 'Noirs'}, {res}. " + (h.get('Termination', '') + ". " if h.get('Termination') not in (None, '', 'Normal') else "") + g['url'])
    p = {"coups": " ".join(toks), "flip": moi == "black", "pendule": pend if any(pend) else None, "infos": infos}
    json.dump(p, open(out, "w"), ensure_ascii=False, indent=1)
    print(infos); print(p["coups"])
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
    san = re.sub(r"=([QRBN])", lambda m: "=" + EN2FR[m.group(1)], san)
    return EN2FR[san[0]] + san[1:] if san[0] in EN2FR else san
def moves_of(txt):
    toks = [t for t in re.sub(r"\d+\.(\.\.)?", " ", txt).split() if t not in ("1-0", "0-1", "1/2-1/2", "*")]
    return [t.rstrip("!?") for t in toks]
def analyse(pj, out):
    import chess, chess.engine
    p = json.load(open(pj)); b = chess.Board(); eng = chess.engine.SimpleEngine.popen_uci(SF)
    res = []
    def sc(x): return x["score"].white().score(mate_score=10000)
    D = int(os.environ.get("DEPTH","20"))
    for k, m in enumerate(moves_of(p["coups"])):
        info = eng.analyse(b, chess.engine.Limit(depth=D), multipv=3)
        best = [[en2fr(b.san(x["pv"][0])), sc(x) / 100, " ".join(en2fr(s) for s in b.variation_san(x["pv"][:8]).split())] for x in info]
        mv = b.parse_san(fr2en(m)); fen = b.fen(); b.push(mv)
        if b.is_checkmate(): after = 10000 if b.turn == chess.BLACK else -10000
        elif b.is_game_over(): after = 0
        else: after = sc(eng.analyse(b, chess.engine.Limit(depth=D)))
        res.append(dict(ply=k, san=m, fen_before=fen, after=after / 100, best=best))
        print(k, m, "après", after / 100, "| meilleurs:", best, flush=True)
    eng.quit(); json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
    stats(out, pj); afficher_ouvertures(moves_of(p["coups"]))
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
    {"setup": lambda: setup(), "analyse": lambda: analyse(*a[1:3]), "stats": lambda: stats(a[1], a[2] if len(a) > 2 else None), "parties": lambda: lister(a[1], int(a[2]) if len(a) > 2 else 10, LI),
     "recuperer": lambda: recuperer(a[1], a[2], a[3] if len(a) > 3 else "partie.json", LI), "ouvertures": lambda: afficher_ouvertures(moves_of(json.load(open(a[1]))["coups"])), "build": lambda: build(*a[1:5])}[a[0]]()
