# Rendu des analyses de parties (procédure technique)

On reprend exactement ce rendu pour chaque analyse écrite. Le document outils/exemple-partie.json montre une analyse complète prête à construire.

## Documents
- outils/modele-analyse.html: modèle de page (styles, script complet), avec des emplacements à remplir: {{TITRE}}, {{ENTETE}}, {{REMARQUES}}, {{BILAN}}, __PLIES__, __VARS__, __FLIP__, __DEPART__, __PIECES__. Les pièces cburnett sont générées au moment du build depuis chess.svg (python-chess).
- outils/outils-analyse.py: installation des outils, analyse Stockfish, construction de la page.
- outils/exemple-partie.json: exemple complet de données, à consulter en cas de doute sur le format.

## Déroulement en étapes groupées
Chaque étape de la conversation (un aller-retour entre Claude et ses outils) relit tout ce qui précède: le coût d'une analyse dépend surtout du nombre d'étapes. Viser sept étapes environ, en lançant dans le même message tout ce qui ne dépend pas d'un résultat précédent. Pas de liste de tâches pour une analyse.
1. Lire en une fois tous les documents utiles: instructions.md, joueur/profil.md, joueur/progression.md, joueur/historique.md, joueur/ouvertures.md, regles/analyse.md, regles/notation.md et ce document. La liste des documents du projet est déjà connue: ne pas la redemander.
2. Une seule commande: clone, copie des outils, setup, écriture de partie.json avec les coups, analyse (en arrière-plan si elle risque de dépasser le délai).
3. Lire le résultat de l'analyse, avec l'indicateur de triche affiché à la fin.
4. Si besoin, vérifier au moteur toutes les affirmations douteuses dans un seul script.
5. Une seule commande: script qui écrit partie.json complet, puis build. Relire ses commentaires avant de lancer la commande, pour ne pas reconstruire la page après coup.
6. Dans le même message: publication de la page et écriture de toutes les fiches joueur (partie, index, et les autres fiches si elles changent).
7. Réponse au joueur.

## Etapes
1. Récupérer les outils sans les recopier: cloner le dépôt dans un dossier de travail (voir instructions.md, section Dépôt GitHub), puis copier depot/outils/modele-analyse.html et depot/outils/outils-analyse.py dans ce dossier avec une commande (cp). Ne pas lire ces deux fichiers: ils sont prêts à l'emploi, et les lire les ferait relire à chaque étape de la conversation. Lire depot/outils/exemple-partie.json seulement en cas de doute sur le format. Si le clone échoue, lire les documents outils/ du projet et les écrire dans le dossier de travail (même nom, sans "outils/"). Avec Claude Code dans un clone local, travailler dans un dossier hors du clone: les fichiers partie.json, analyse.json et page.html d'une analyse ne doivent jamais se retrouver dans le dépôt.
2. `python3 outils-analyse.py setup`: installe python-chess (si pip normal échoue: passage par la wheel chess-1.10.0) et Stockfish 17.1 dans ~/sf (téléchargé depuis GitHub).
3. Ecrire partie.json avec au minimum "coups" (notation française, ex. "1.e4 e5 2.Cf3 ..."; un PGN en notation anglaise est à traduire: K R, Q D, R T, B F, N C).
4. `python3 outils-analyse.py analyse partie.json analyse.json`: pour chaque demi-coup, éval après le coup et 3 meilleurs coups avant, avec la suite. Relire ces lignes pour rédiger: étiquette et commentaire de chaque coup, variantes, remarques, bilan. Vérifier au moteur toute affirmation (multipv avec root_moves pour comparer un coup précis). Pour les vérifications, lancer python avec -u et un timeout; ne pas analyser une position déjà mate (le script plante). La commande affiche à la fin l'indicateur de triche des deux camps; `python3 outils-analyse.py stats analyse.json` le réaffiche.
5. Compléter partie.json (champs: titre, flip, depart, entete, coups, commentaires, variantes, remarques, bilan). "commentaires" est un dictionnaire dont les clés sont les coups commentés en notation française ("1.d4", "11...Cc6"; signes +, #, ! et ? facultatifs). Les coups absents n'ont pas de commentaire et gardent l'étiquette automatique, affichée par la commande analyse (voir regles/analyse.md). Chaque commentaire: "text", et en option "tag" (pour corriger l'étiquette automatique: excellent, bon, imprecis, erreur, gaffe), "best" (meilleur coup en notation française) et "rouge" (liste de flèches [case de départ, case d'arrivée]). Variantes: liste vide par défaut, remplie seulement si le joueur les demande. Chaque variante: "nom", "avant" (indice du demi-coup avant lequel elle part, 0 = position initiale), "coups", "notes" (une note pour la position de départ puis une par coup), "rouge" (flèches par étape, clés "0", "1"...). "entete", "remarques" et "bilan" sont des fragments HTML (classes eyebrow, players, mono, result, cols, card, key). Plus simple: un petit script Python qui écrit partie.json (pas d'échappement à la main).
6. `python3 outils-analyse.py build partie.json analyse.json modele-analyse.html page.html` (le build vérifie lui-même la syntaxe du script de la page), puis publier page.html avec l'outil Artifact (icône "chess", titre court: le thème clé de la partie, ex. "Fourchette en d5"). Le build rejoue toutes les variantes: un coup illégal signale une erreur de raisonnement.

Variantes demandées après coup, dans la même conversation: ajouter "variantes" à partie.json, relancer build et republier le même fichier, en une seule étape. Dans une autre conversation, les fichiers de travail n'existent plus: il faut refaire l'analyse.

## Ce que le rendu doit garder
- Echiquier: cases beige et marron (#f0d9b5, #b58863), pièces SVG cburnett, cases fixes de 44 px (40 px sous 384 px de large), retourné quand le joueur a les Noirs ("flip": true).
- Sous l'échiquier, une seule ligne de 5 boutons: début, précédent, bouton vert "Meilleur coup" (devient "Coup joué"), suivant, fin. Le bouton vert est actif sur tous les coups: il montre la position avant le coup avec le meilleur coup en flèche verte.
- Juste sous les boutons: une phrase qui dit ce qui est affiché ("Position après ...", "Position avant ..., meilleur coup ...").
- Puis, directement, la carte du coup: coup, symbole, étiquette (excellent, bon, imprécis, erreur, gaffe), traduction en clair, commentaire, et la ligne systématique "Meilleur coup selon le moteur: ..." (précise "c'est le coup joué" si c'est le cas). Sur téléphone, l'échiquier et le commentaire doivent être visibles en même temps.
- Courbe d'évaluation après le commentaire (jamais entre l'échiquier et le commentaire), puis feuille de partie cliquable, légende.
- Sections suivantes: "Réponses aux remarques" (citations du joueur), "Variantes expliquées" (second échiquier, onglets, boutons précédent et suivant; section absente quand il n'y a pas de variante), "Bilan de la partie" (deux cartes et une leçon clé).
- Flèches rouges pour menaces, lignes, clouages; flèche verte uniquement pour le meilleur coup.

## A éviter
- Petits boutons, bouton "Position avant le coup" séparé, bouton du meilleur coup absent sur certains coups ou placé loin de l'échiquier.
- Commentaire placé sous la courbe d'évaluation.
- Symboles Unicode des pièces (échiquier déformé et difficile à lire).
