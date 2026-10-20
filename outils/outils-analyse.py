#!/usr/bin/env python3
"""Outils pour l'analyse des parties d'échecs (page interactive coup par coup).

Usage:
  python3 outils-analyse.py setup
  python3 outils-analyse.py analyse partie.json analyse.json
  python3 outils-analyse.py build partie.json analyse.json modele-analyse.html sortie.html
Voir outils/rendu-analyse.md. Si le modèle contient __PIECES__, les pièces cburnett sont
générées depuis chess.svg (python-chess) au lieu d'être recopiées en base64.
"""
import base64, json, os, re, subprocess, sys

HOME = os.path.expanduser("~")
SF = os.path.join(HOME, "sf", "stockfish", "stockfish-ubuntu-x86-64-avx2")
FR2EN = {"R": "K", "D": "Q", "T": "R", "F": "B", "C": "N"}
EN2FR = {"K": "R", "Q": "D", "R": "T", "B": "F", "N": "C"}


def setup():
    d = os.path.join(HOME, "sf"); os.makedirs(d, exist_ok=True)
    subprocess.run(f"pip download chess==1.10.0 --no-deps -d {d} -q && pip install --break-system-packages -q {d}/chess-1.10.0-py3-none-any.whl", shell=True, check=True)
    if not os.path.exists(SF):
        subprocess.run(f"cd {d} && curl -sSL -o sf.tar https://github.com/official-stockfish/Stockfish/releases/download/sf_17.1/stockfish-ubuntu-x86-64-avx2.tar && tar xf sf.tar && chmod +x {SF}", shell=True, check=True)
    print("ok", SF)


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
    def sc(x):
        return x["score"].white().score(mate_score=10000)
    for k, m in enumerate(moves_of(p["coups"])):
        info = eng.analyse(b, chess.engine.Limit(depth=int(os.environ.get("DEPTH","20"))), multipv=3)
        best = [[en2fr(b.san(x["pv"][0])), sc(x) / 100, " ".join(en2fr(s) for s in b.variation_san(x["pv"][:8]).split())] for x in info]
        mv = b.parse_san(fr2en(m)); fen = b.fen(); b.push(mv)
        after = sc(eng.analyse(b, chess.engine.Limit(depth=int(os.environ.get("DEPTH","20")))))
        res.append(dict(ply=k, san=m, fen_before=fen, after=after / 100, best=best))
        print(k, m, "après", after / 100, "| meilleurs:", best)
    eng.quit(); json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)


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


def build(pj, aj, tpl, out):
    import chess
    p = json.load(open(pj)); an = json.load(open(aj)); mv_list = moves_of(p["coups"])
    assert len(p["commentaires"]) == len(mv_list) == len(an), "un commentaire par demi-coup"
    b = chess.Board(); PL = [{"fen": b.board_fen(), "eval": 0.3, "mate": None}]; befores = []
    for k, m in enumerate(mv_list):
        c = p["commentaires"][k]; mv = b.parse_san(fr2en(m)); before = b.board_fen(); befores.append(b.fen())
        bsan = c.get("best") or an[k]["best"][0][0]; bm = b.parse_san(fr2en(bsan))
        cl = clair(b, mv); san = en2fr(b.san(mv)); b.push(mv)
        ev = an[k]["after"]; ev = max(-100, min(100, ev))
        PL.append({"num": k // 2 + 1, "side": "B" if k % 2 == 0 else "N", "san": san, "clair": cl,
                   "fen": b.board_fen(), "before": before, "frm": mv.uci()[:2], "to": mv.uci()[2:4],
                   "eval": round(ev, 1), "mate": None, "tag": c["tag"], "text": c["text"],
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
    if "__PIECES__" in h:
        h = h.replace("__PIECES__", pieces_js())
    open(out, "w").write(h); print("ok", out, len(h))


if __name__ == "__main__":
    a = sys.argv[1:]
    {"setup": lambda: setup(), "analyse": lambda: analyse(*a[1:3]), "build": lambda: build(*a[1:5])}[a[0]]()
