# Analyse d'une partie

S'applique aux parties jouées avec Claude comme aux parties jouées en ligne et envoyées en PGN.

## Plusieurs parties envoyées d'un coup
D'abord un tri rapide au moteur (résultat, coup qui fait basculer chaque partie, lien avec le thème en cours), puis une page d'analyse par partie.

## Vérification
- Rejouer et vérifier la partie avec un moteur (Stockfish) avant de rédiger l'analyse.
- Vérifier chaque affirmation, y compris les variantes proposées, en contrôlant pour chaque coup proposé toutes les pièces adverses qui voient la case d'arrivée.
- Si le moteur n'est pas disponible, le dire clairement et présenter l'analyse comme faite de tête.
- Honnêteté sur les erreurs de Claude aussi, pendant la partie comme dans l'analyse.

## Contenu
- Commentaire pour chaque coup, y compris ceux de Claude, avec une étiquette: excellent, bon, imprécis, erreur, gaffe.
- Un coup qui perd plus d'un point mais laisse une position presque égale est noté imprécis; l'étiquette erreur est gardée pour les pertes réelles. Un mat raté quand la position reste largement gagnante est noté imprécis.
- Pour chaque coup, une ligne systématique "Meilleur coup selon le moteur: ...".
- Quand un coup est une erreur, proposer la meilleure alternative et l'expliquer.
- Répondre à chaque remarque faite par le joueur pendant la partie, en citant la remarque.
- Section "Variantes expliquées" pour rejouer les lignes proposées coup par coup.
- Bilan en fin de page: points positifs, points à retenir, une leçon clé.

## Forme
- Page d'analyse interactive, construite selon outils/rendu-analyse.md.
- Explications simples et concrètes, sans théorie inutile, en nommant les pièces et les cases.
- Echiquier retourné quand le joueur a les Noirs.
