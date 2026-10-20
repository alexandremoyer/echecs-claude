# Rendu des analyses de parties (procédure technique)

On reprend exactement ce rendu pour chaque analyse écrite. Le document outils/exemple-partie.json montre une analyse complète prête à construire.

## Documents
- outils/modele-analyse.html: modèle de page (styles, script complet), avec des emplacements à remplir: {{TITRE}}, {{ENTETE}}, {{REMARQUES}}, {{BILAN}}, __PLIES__, __VARS__, __FLIP__, __DEPART__, __PIECES__. Les pièces cburnett sont générées au moment du build depuis chess.svg (python-chess).
- outils/outils-analyse.py: installation des outils, analyse Stockfish, construction de la page.
- outils/exemple-partie.json: exemple complet de données, à copier comme point de départ.

## Etapes
1. Lire les trois documents outils/modele-analyse.html, outils/outils-analyse.py et outils/exemple-partie.json et les écrire dans un dossier de travail (même nom, sans "outils/"). Avec Claude Code dans un clone local, travailler dans un dossier hors du clone: les fichiers partie.json, analyse.json et page.html d'une analyse ne doivent jamais se retrouver dans le dépôt.
2. `python3 outils-analyse.py setup`: installe python-chess (si pip normal échoue: passage par la wheel chess-1.10.0) et Stockfish 17.1 dans ~/sf (téléchargé depuis GitHub).
3. Ecrire partie.json avec au minimum "coups" (notation française, ex. "1.e4 e5 2.Cf3 ..."; un PGN en notation anglaise est à traduire: K R, Q D, R T, B F, N C).
4. `python3 outils-analyse.py analyse partie.json analyse.json`: pour chaque demi-coup, éval après le coup et 3 meilleurs coups avant, avec la suite. Relire ces lignes pour rédiger: étiquette et commentaire de chaque coup, variantes, remarques, bilan. Vérifier au moteur toute affirmation (multipv avec root_moves pour comparer un coup précis). Pour les vérifications, lancer python avec -u et un timeout; ne pas analyser une position déjà mate (le script plante).
5. Compléter partie.json (champs: titre, flip, depart, entete, coups, commentaires, variantes, remarques, bilan; voir l'exemple): un commentaire par demi-coup, y compris les coups de Claude. Plus simple: un petit script Python qui écrit partie.json (pas d'échappement à la main).
6. `python3 outils-analyse.py build partie.json analyse.json modele-analyse.html page.html`, vérifier la syntaxe du script (node, new Function), puis publier page.html avec l'outil Artifact (icône "chess", titre court: le thème clé de la partie, ex. "Fourchette en d5"). Le build rejoue toutes les variantes: un coup illégal signale une erreur de raisonnement.

## Ce que le rendu doit garder
- Echiquier: cases beige et marron (#f0d9b5, #b58863), pièces SVG cburnett, cases fixes de 44 px (40 px sous 384 px de large), retourné quand le joueur a les Noirs ("flip": true).
- Sous l'échiquier, une seule ligne de 5 boutons: début, précédent, bouton vert "Meilleur coup" (devient "Coup joué"), suivant, fin. Le bouton vert est actif sur tous les coups: il montre la position avant le coup avec le meilleur coup en flèche verte.
- Juste sous les boutons: une phrase qui dit ce qui est affiché ("Position après ...", "Position avant ..., meilleur coup ...").
- Puis, directement, la carte du coup: coup, symbole, étiquette (excellent, bon, imprécis, erreur, gaffe), traduction en clair, commentaire, et la ligne systématique "Meilleur coup selon le moteur: ..." (précise "c'est le coup joué" si c'est le cas). Sur téléphone, l'échiquier et le commentaire doivent être visibles en même temps.
- Courbe d'évaluation après le commentaire (jamais entre l'échiquier et le commentaire), puis feuille de partie cliquable, légende.
- Sections suivantes: "Réponses aux remarques" (citations du joueur), "Variantes expliquées" (second échiquier, onglets, boutons précédent et suivant), "Bilan de la partie" (deux cartes et une leçon clé).
- Flèches rouges pour menaces, lignes, clouages; flèche verte uniquement pour le meilleur coup.

## A éviter
- Petits boutons, bouton "Position avant le coup" séparé, bouton du meilleur coup absent sur certains coups ou placé loin de l'échiquier.
- Commentaire placé sous la courbe d'évaluation.
- Symboles Unicode des pièces (échiquier déformé et difficile à lire).
