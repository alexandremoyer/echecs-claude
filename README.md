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
Trois façons d'installer:

| Installation | Règles et outils | Fiches du joueur | Contribuer par pull request |
|---|---|---|---|
| A. Projet claude.ai avec clone (conseillée) | Clone du fork, à jour à chaque conversation | Documents du projet | Oui |
| B. Projet claude.ai sans GitHub | Documents du projet, recopiés à la main | Documents du projet | Non |
| C. Claude Code sur sa machine | Clone du fork | Dossier joueur/ du clone | Oui |

### A. Projet claude.ai avec clone du dépôt
Demande un compte GitHub relié à claude.ai (réglages, rubrique Connecteurs), avec accès au fork.
1. Forker le dépôt sur GitHub. Le fork se met à jour depuis ce dépôt avec le bouton "Sync fork".
2. Dans claude.ai, créer un projet (par exemple "Echecs").
3. Dans les instructions du projet, coller, en remplaçant le nom du fork:
   ```
   Au début de chaque conversation, cloner le dépôt GitHub mon-pseudo/echecs-claude, puis lire instructions.md et suivre ses règles. Les fiches joueur/ sont des documents du projet, pas des fichiers du clone.
   ```
4. Ouvrir une conversation dans le projet et écrire "Initialise mon profil". Claude clone le fork, crée les fiches joueur/ dans les documents du projet et pose quelques questions (niveau, classement, plateforme, notation, objectifs).

Chaque conversation repart d'un environnement vierge: Claude reclone le dépôt au début, ce qui prend quelques secondes. Les fiches du joueur, elles, restent dans le projet.

### B. Projet claude.ai sans GitHub
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
5. Dans une nouvelle conversation, écrire "Initialise mon profil". Claude crée les fiches joueur/ et pose quelques questions.

### C. Claude Code sur sa machine
1. Forker le dépôt et le cloner sur sa machine.
2. Lancer Claude Code dans le clone: le fichier CLAUDE.md, lu automatiquement, renvoie vers instructions.md.
3. Ecrire "Initialise mon profil": Claude crée le dossier joueur/ dans le clone, exclu des commits par le .gitignore.

## Utilisation
- **Jouer une partie**: ouvrir une nouvelle conversation dans le projet pour chaque partie. Claude demande la couleur (ou un tirage au sort), l'ouverture éventuelle et le thème éventuel.
- **Analyser une partie en ligne**: coller le PGN (sur chess.com ou Lichess, bouton de partage puis PGN). Plusieurs PGN peuvent être envoyés dans la même conversation.
- **Suivi**: après chaque partie ou analyse, Claude met à jour les fiches joueur/. On peut les relire et les corriger à tout moment.

## Mettre à jour les règles
- **Installations A et C**: synchroniser le fork sur GitHub ("Sync fork"). Avec A, la conversation suivante utilise directement la nouvelle version; avec C, faire un `git pull` dans le clone.
- **Installation B**: télécharger la nouvelle version du dépôt et demander à Claude de réenregistrer les documents regles/, outils/, modeles/ et instructions.md.

Dans tous les cas, les fiches joueur/ ne sont pas touchées.

## Contribuer
Les améliorations des règles et des outils sont les bienvenues, par issue ou pull request.

Pendant les parties et les analyses, Claude ne modifie pas les documents communs: s'il repère une règle à améliorer, il la propose. Pour la soumettre:
1. Dans une conversation qui a cloné son fork (installation A ou C), demander explicitement à Claude d'appliquer la modification, par exemple "Ajoute cette règle dans regles/partie.md et prépare une pull request".
2. Claude crée une branche, fait le commit, la pousse sur le fork et ouvre la pull request vers ce dépôt.
3. Vérifier avant l'envoi que la modification ne contient aucune donnée personnelle (parties, pseudo, classement): ces informations restent dans joueur/.

## Remarques
- Les pages d'analyse demandent que la session de Claude puisse installer des paquets Python et télécharger Stockfish depuis GitHub. Sinon, Claude analyse quand même la partie, mais sans moteur, et doit le préciser.
- Pièces de l'échiquier: jeu cburnett de Colin M.L. Burnett. Moteur: Stockfish.
