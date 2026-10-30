# Analyse d'une partie

S'applique aux parties jouées avec Claude comme aux parties jouées en ligne et envoyées en PGN.

## Parties chess.com et lichess
- Si le joueur ne donne pas de PGN, récupérer la partie avec son pseudo (pseudos dans joueur/profil.md; voir outils/rendu-analyse.md, commandes parties et recuperer, option --lichess). Sans précision du joueur, prendre sa plateforme principale indiquée dans le profil. Si le domaine (api.chess.com ou lichess.org) est inaccessible, demander le PGN.
- Quand la pendule est connue, la commenter: temps restant, coups joués trop vite ou trop lentement, erreurs jouées en quelques secondes. Le bilan dit si la pendule a joué un rôle.

## Plusieurs parties envoyées d'un coup
D'abord un tri rapide au moteur (résultat, coup qui fait basculer chaque partie, lien avec le thème en cours), puis une page d'analyse par partie.

## Vérification
- Rejouer et vérifier la partie avec un moteur (Stockfish) avant de rédiger l'analyse.
- Vérifier chaque affirmation, y compris les variantes proposées, en contrôlant pour chaque coup proposé toutes les pièces adverses qui voient la case d'arrivée.
- Si le moteur n'est pas disponible, le dire clairement et présenter l'analyse comme faite de tête.
- Honnêteté sur les erreurs de Claude aussi, pendant la partie comme dans l'analyse.

## Contenu
- Etiquette pour chaque coup (excellent, bon, imprécis, erreur, gaffe), calculée automatiquement d'après la perte mesurée par le moteur, et corrigée à la main si besoin. "Excellent" est toujours donné à la main.
- Calcul: perte jusqu'à 0,5 point, bon; jusqu'à 1 point, imprécis; jusqu'à 2,5 points, erreur, ou imprécis si la position reste presque égale (moins d'un point d'écart); plus de 2,5 points, gaffe, ou erreur si le camp qui joue reste nettement mieux (1,5 point ou plus). Avec un gros avantage (5 points ou plus après le coup), un mat raté ou une perte est noté imprécis; avec un gros retard (5 points ou plus avant le coup), une perte jusqu'à 2,5 points aussi.
- Commentaire seulement pour les coups qui comptent: erreurs et gaffes, coups excellents ou marquants, tournants de la partie, coups d'ouverture, y compris les coups de Claude dans une partie jouée avec lui. Les autres coups gardent la traduction en clair et la ligne du meilleur coup, sans commentaire.
- Pour chaque coup, une ligne systématique "Meilleur coup selon le moteur: ..." (automatique).
- Ouverture: le nom de l'ouverture et de la variante est reconnu automatiquement par position (base d'ouvertures lichess) et affiché sur chaque coup de la théorie, comme la sortie de la théorie. Commentaires: le coup qui définit l'ouverture la nomme; chaque changement de variante est confirmé (gambit accepté ou refusé, variante d'avance...); un ordre de coups inhabituel qui revient dans la théorie est signalé; le coup qui sort de la théorie est commenté (qui en sort, et si c'est une bonne idée). Les noms de la base sont en partie en anglais: les traduire dans les commentaires.
- Quand un coup est une erreur, proposer la meilleure alternative et l'expliquer.
- Répondre à chaque remarque faite par le joueur pendant la partie, en citant la remarque.
- Variantes expliquées (lignes à rejouer coup par coup): désactivées par défaut. Seulement si le joueur les demande, de préférence dans la même conversation (ajout peu coûteux, voir outils/rendu-analyse.md).
- Bilan en fin de page: points positifs, points à retenir, une leçon clé.

## Forme
- Page d'analyse interactive, construite selon outils/rendu-analyse.md.
- Explications simples et concrètes, sans théorie inutile, en nommant les pièces et les cases.
- Echiquier retourné quand le joueur a les Noirs.

## Organisation
- Travail en étapes groupées, sans liste de tâches: voir outils/rendu-analyse.md, section "Déroulement en étapes groupées".
