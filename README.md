# Echecs avec Claude

Un projet claude.ai pour progresser aux échecs avec Claude:
- jouer des parties dans la conversation, à l'écrit ou en mode vocal;
- faire analyser ses parties jouées en ligne (PGN de chess.com ou Lichess);
- obtenir pour chaque partie une page d'analyse interactive, vérifiée avec le moteur Stockfish;
- garder un suivi de sa progression: ouvertures, points faibles, historique des parties.

## Contenu du dépôt
```
CLAUDE.md            renvoi vers instructions.md pour Claude Code
instructions.md      point d'entrée lu par Claude
regles/              règles communes (partie, mode vocal, analyse, notation)
outils/              procédure, modèle de page, script et exemple d'analyse
modeles/             fiches vides du joueur, copiées à l'initialisation
joueur/              fiches personnelles (non versionné)
```

Les règles et les outils sont communs. Les données personnelles vivent dans joueur/, qui n'est pas versionné: chacun garde ses parties pour lui.

## Installation
Deux façons d'installer:
- **Projet claude.ai**: le plus simple, sans compte GitHub. Les fiches du joueur vivent dans le projet.
- **Fork du dépôt**: pratique pour proposer des modifications par pull request (voir plus bas).

### Projet claude.ai
1. Dans claude.ai, créer un projet (par exemple "Echecs").
2. Dans les instructions du projet, coller:
   ```
   Lire instructions.md au début de chaque conversation et suivre ses règles.
   ```
3. Télécharger le dépôt (bouton "Code" puis "Download ZIP").
4. Ouvrir une conversation dans le projet, joindre le ZIP et demander:
   ```
   Enregistre chaque fichier de ce ZIP comme document du projet, au même chemin (instructions.md, regles/..., outils/..., modeles/...), sans README.md, CLAUDE.md ni .gitignore.
   ```
   Les fichiers doivent être des documents du projet écrits par Claude, et non de simples fichiers déposés dans les connaissances du projet: c'est ce qui permet à Claude de créer puis de mettre à jour les fiches du joueur.
5. Dans une nouvelle conversation, écrire "Initialise mon profil". Claude crée les fiches joueur/ et pose quelques questions (niveau, classement, plateforme, notation, objectifs).

### Fork du dépôt
1. Forker le dépôt sur GitHub.
2. Faire cloner le fork par Claude: avec Claude Code sur sa machine, ou dans une session Claude reliée à son compte GitHub. Le fichier CLAUDE.md, lu automatiquement par Claude Code, renvoie vers instructions.md.
3. Ecrire "Initialise mon profil": Claude crée le dossier joueur/ dans le clone.

Où garder les fiches du joueur:
- **Claude Code sur sa machine**: le dossier joueur/ reste sur le disque, exclu des commits par le .gitignore.
- **Session Claude dans le cloud**: l'environnement est effacé après inactivité, et joueur/ disparaîtrait avec lui. Dans ce cas, garder les fiches dans un projet claude.ai (installation ci-dessus) et n'utiliser le fork que pour contribuer.

## Utilisation
- **Jouer une partie**: ouvrir une nouvelle conversation dans le projet pour chaque partie. Claude demande la couleur (ou un tirage au sort), l'ouverture éventuelle et le thème éventuel.
- **Analyser une partie en ligne**: coller le PGN (sur chess.com ou Lichess, bouton de partage puis PGN). Plusieurs PGN peuvent être envoyés dans la même conversation.
- **Suivi**: après chaque partie ou analyse, Claude met à jour les fiches joueur/. On peut les relire et les corriger à tout moment.

## Mettre à jour les règles
Télécharger la nouvelle version du dépôt et demander à Claude de réenregistrer les documents regles/, outils/, modeles/ et instructions.md. Les fiches joueur/ ne sont pas touchées.

## Contribuer
Les améliorations des règles et des outils sont les bienvenues, par issue ou pull request.

Pendant les parties et les analyses, Claude ne modifie pas les documents communs: s'il repère une règle à améliorer, il la propose. Pour la soumettre:
1. Depuis un clone de son fork, demander explicitement à Claude d'appliquer la modification, par exemple "Ajoute cette règle dans regles/partie.md et prépare une pull request".
2. Claude crée une branche, fait le commit, la pousse sur le fork et ouvre la pull request vers ce dépôt.
3. Vérifier avant l'envoi que la modification ne contient aucune donnée personnelle (parties, pseudo, classement): ces informations restent dans joueur/.

## Remarques
- Les pages d'analyse demandent que la session de Claude puisse installer des paquets Python et télécharger Stockfish depuis GitHub. Sinon, Claude analyse quand même la partie, mais sans moteur, et doit le préciser.
- Pièces de l'échiquier: jeu cburnett de Colin M.L. Burnett. Moteur: Stockfish.
