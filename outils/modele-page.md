# Modèle de page d'analyse

A lire seulement pour modifier le modèle outils/modele-analyse.html ou le script qui le remplit. Pendant une analyse, la page est construite par le script sans que ce document soit nécessaire.

## Emplacements du modèle
{{TITRE}}, {{ENTETE}}, {{REMARQUES}}, {{BILAN}}, __PLIES__, __VARS__, __FLIP__, __DEPART__, __PIECES__. Les pièces cburnett sont générées au moment du build depuis chess.svg (python-chess). Le document outils/exemple-partie.json montre des données complètes prêtes à construire, variantes comprises.

## Ce que le rendu doit garder
- Echiquier: cases beige et marron (#f0d9b5, #b58863), pièces SVG cburnett, cases fixes de 44 px (40 px sous 384 px de large), retourné quand le joueur a les Noirs ("flip": true).
- Sous l'échiquier, une seule ligne de 5 boutons: début, précédent, bouton vert "Meilleur coup" (devient "Coup joué"), suivant, fin. Le bouton vert est actif sur tous les coups: il montre la position avant le coup avec le meilleur coup en flèche verte.
- Juste sous les boutons: une phrase qui dit ce qui est affiché ("Position après ...", "Position avant ..., meilleur coup ...").
- Puis, directement, la carte du coup: coup, symbole, étiquette (excellent, bon, imprécis, erreur, gaffe), traduction en clair, ligne "Théorie" (ouverture et variante) tant que la partie est dans la théorie (puis "Sortie de la théorie"), ligne "Pendule" quand elle est connue, commentaire (absent pour un coup sans commentaire), et la ligne systématique "Meilleur coup selon le moteur: ..." (précise "c'est le coup joué" si c'est le cas). Quand le meilleur coup est une idée manquée déjà signalée à un coup précédent, la ligne devient "Meilleur coup en dehors de ..., déjà signalé au coup ...: ..." et le bouton vert montre ce meilleur autre coup. Sur téléphone, l'échiquier et le commentaire doivent être visibles en même temps.
- Courbe d'évaluation après le commentaire (jamais entre l'échiquier et le commentaire), puis feuille de partie cliquable, légende.
- Sections suivantes: "Réponses aux remarques" (citations du joueur), "Variantes expliquées" (second échiquier, onglets, boutons précédent et suivant; section absente quand il n'y a pas de variante), "Bilan de la partie" (deux cartes et une leçon clé).
- Flèches rouges pour menaces, lignes, clouages; flèche verte uniquement pour le meilleur coup.

## A éviter
- Petits boutons, bouton "Position avant le coup" séparé, bouton du meilleur coup absent sur certains coups ou placé loin de l'échiquier.
- Commentaire placé sous la courbe d'évaluation.
- Symboles Unicode des pièces (échiquier déformé et difficile à lire).
