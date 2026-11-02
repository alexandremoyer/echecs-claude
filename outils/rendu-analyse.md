# Outils d'analyse (référence technique)

Le déroulement d'une analyse est dans regles/analyse.md. Ce document décrit les commandes et les champs, pour les cas qui sortent du déroulement courant. Les outils viennent du clone du dépôt (outils/modele-analyse.html, outils/outils-analyse.py, outils/exemple-partie.json): ils ne sont pas lus, seulement copiés dans le dossier de travail. Si le clone échoue, l'analyse se fait sans moteur, et le joueur en est prévenu. Avec Claude Code dans un clone local, travailler dans un dossier hors du clone: les fichiers d'une analyse ne doivent jamais se retrouver dans le dépôt.

## Commandes
- `analyser PSEUDO CHOIX [--lichess]`: setup si besoin (python-chess, Stockfish 17.1 dans ~/sf, base d'ouvertures lichess dans ~/sf/ouvertures), récupération de la partie (partie.json), analyse (analyse.json), affichage complet et squelette des champs à rédiger. CHOIX: rang dans la liste des dernières parties (1 = la plus récente), pseudo de l'adversaire (partie la plus récente contre lui) ou lien de la partie (un lien lichess suffit sans --lichess). Nécessite api.chess.com ou lichess.org dans les domaines autorisés de claude.ai. Budget de temps du moteur: variable BUDGET (90 s par défaut, réduit du temps d'installation), pour tenir sous le délai de 120 s.
- `analyser [PSEUDO|noirs] --pgn fichier.pgn`: même chose pour un PGN collé par le joueur, écrit dans un fichier au préalable. Le pseudo (comparé aux en-têtes White et Black) ou le mot "noirs" donne la couleur du joueur; par défaut, Blancs. Les coups sont traduits en français par le script.
- `verifier partie.json SPEC...`: pour chaque SPEC, les trois meilleurs coups avec évaluation (mats en clair) et suite. SPEC: `9...Te8` (position avant ce coup), `+9...Te8` (après), `9...Te8:exd4,Te8` (évalue aussi ces coups précis, en français). Temps par position: variable T (4 s), limité par BUDGET.
- `build partie.json analyse.json modele-analyse.html page.html`: fusionne complement.json dans partie.json s'il existe, écrit la page (syntaxe du script vérifiée avec node), puis fiche.md et index.txt si partie.json contient numero. Rejoue toutes les variantes: un coup illégal signale une erreur de raisonnement.
- Aussi: `parties PSEUDO [N] [--lichess]` (liste des N dernières parties), `recuperer PSEUDO CHOIX [partie.json]`, `importer fichier.pgn [PSEUDO]`, `analyse partie.json analyse.json`, `stats analyse.json [partie.json]` (indicateur, étiquettes, mats manqués), `ouvertures partie.json`, `fiche partie.json analyse.json`.

## Champs de complement.json
Fusionnés dans partie.json par build; les champs absents sont complétés. Ecrire le fichier avec `cat > complement.json <<'EOF' ... EOF` dans la commande du build (pas de script Python). Le squelette affiché par analyser reprend ces champs avec les joueurs déjà remplis.
- "numero": numéro de la partie (dernier numéro de l'index + 1, archives comprises).
- "titre": thème clé de la partie, 2 à 4 mots (ex. "Fourchette en d5").
- "entete": fragment HTML (classes eyebrow, players, mono, result): plateforme et date, couleur, joueurs et classements, ouverture et premiers coups, résultat.
- "commentaires": dictionnaire dont les clés sont les coups commentés en notation française ("1.d4", "11...Cc6"; signes +, #, ! et ? facultatifs). Chaque commentaire: "text", et en option "tag" (pour corriger l'étiquette automatique: excellent, bon, imprecis, erreur, gaffe), "best" (meilleur coup en notation française, si différent de celui du moteur) et "rouge" (liste de flèches [case de départ, case d'arrivée]).
- "bilan": fragment HTML (classes cols, card, key): deux cartes (points positifs, à retenir) et une leçon clé.
- "remarques": fragment HTML, réponses aux remarques du joueur (facultatif).
- "lecons": liste de phrases pour la fiche de la partie. "mots_cles": liste de 5 à 6 mots-clés pour l'index.
- "variantes": liste vide par défaut. Chaque variante: "nom", "avant" (indice du demi-coup avant lequel elle part, 0 = position initiale), "coups" (notation française), "notes" (une note pour la position de départ puis une par coup), "rouge" (flèches par étape, clés "0", "1"...).
- "depart" (phrase sur la position initiale) et "flip" (échiquier retourné) sont remplis par recuperer ou importer, ou complétés par build.

Champs écrits par recuperer ou importer: "coups" (notation française, "1.e4 e5 2.Cf3 ..."), "flip", "pendule" ([temps restant, temps du coup] en secondes, par demi-coup), "infos" (phrase récapitulative), "meta" (plateforme, joueurs, classements, date, cadence, couleur, résultat, nombre de coups, lien).

## Fichiers produits par build
- page.html: la page d'analyse, à envoyer au joueur avec SendUserFile (affichage inline). Artifact seulement sur demande.
- fiche.md: fiche joueur/parties/partie-NNN.md, d'après modeles/partie.md: en-tête, joueurs, coups, leçons, pendule, indicateur de triche, mats manqués. A écrire dans le projet par local_path, sans la relire.
- index.txt: ligne d'index à ajouter à joueur/historique.md (format de modeles/historique.md).

## Format des évaluations
Evaluations du point de vue des Blancs, en points. Mats affichés en clair ("mat en 3 pour les Noirs"). Après un coup qui mate, l'évaluation vaut +100 ou -100; après une nulle, 0. Pour les vérifications, lancer python avec -u et un timeout.
