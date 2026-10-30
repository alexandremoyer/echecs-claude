# Echecs avec Claude

Un projet claude.ai pour progresser aux échecs avec Claude:
- jouer des parties dans la conversation, à l'écrit ou en mode vocal;
- faire analyser ses parties jouées en ligne (récupérées directement sur chess.com avec son pseudo, ou PGN de chess.com ou Lichess);
- obtenir pour chaque partie une page d'analyse interactive, vérifiée avec le moteur Stockfish: étiquette de chaque coup, commentaires sur les coups importants, suivi de l'ouverture et de ses variantes, pendule (parties chess.com récupérées), variantes à rejouer sur demande;
- garder un suivi de sa progression: ouvertures, points faibles, historique des parties.

## Contenu du dépôt
```
CLAUDE.md            consignes pour Claude quand il travaille dans un clone du dépôt
instructions.md      point d'entrée lu par Claude
regles/              règles communes (partie, mode vocal, analyse, notation)
outils/              procédure, modèle de page, script et exemple d'analyse
modeles/             fiches vides du joueur, copiées à l'initialisation
```

Les règles et les outils sont communs. Les données personnelles (fiches joueur/) ne sont jamais versionnées: elles vivent dans le projet claude.ai de chacun.

## Principe
Tout ce que Claude utilise au quotidien est stocké dans les documents du projet claude.ai: les règles et les outils copiés depuis ce dépôt, et les fiches du joueur. GitHub sert aussi:
- pour récupérer les outils d'analyse (modèle de page, script) sans les recopier dans la conversation, ce qui réduit le coût d'une analyse;
- pour importer les règles à l'installation;
- pour les mettre à jour quand le dépôt évolue;
- pour proposer une amélioration par pull request.

Dans tous ces cas, Claude clone le dépôt le temps de la conversation (le dépôt d'origine, ou le fork indiqué dans le profil du joueur). Le clone est effacé ensuite, les documents du projet restent.

Parties chess.com: Claude peut récupérer une partie directement avec le pseudo du joueur (API publique de chess.com), pendule comprise, si le domaine api.chess.com est autorisé dans les réglages de claude.ai (voir Installation, étape 4). Sinon, on lui colle le PGN.

## Installation
1. Dans claude.ai, créer un projet (par exemple "Echecs").
2. Dans les instructions du projet, coller:
   ```
   Lire claude/instructions.md au début de chaque conversation et suivre ses règles.
   ```
   Un document enregistré à la racine du projet est automatiquement rangé dans le dossier claude/: instructions.md devient donc claude/instructions.md, les autres documents gardent leur chemin (regles/..., outils/..., modeles/...).
3. Ouvrir une conversation dans le projet et importer les règles, au choix:
   - **avec GitHub relié à claude.ai** (réglages, rubrique Connecteurs): demander "Clone le dépôt alexandremoyer/echecs-claude et enregistre chaque fichier comme document du projet, au même chemin, sauf README.md, CLAUDE.md et .gitignore". Pour pouvoir contribuer ensuite, forker d'abord le dépôt et donner le nom de son fork à la place.
   - **sans GitHub**: télécharger le dépôt (bouton "Code" puis "Download ZIP"), le joindre et demander "Enregistre chaque fichier de ce ZIP comme document du projet, au même chemin, sauf README.md, CLAUDE.md et .gitignore".

   Les fichiers doivent être des documents du projet écrits par Claude, et non de simples fichiers déposés dans les connaissances du projet: c'est ce qui permet à Claude de créer puis de mettre à jour les fiches du joueur.
4. Facultatif, pour que Claude récupère lui-même les parties chess.com: autoriser le domaine `api.chess.com`. Sur claude.ai, dans un navigateur: Paramètres, Capacités, liste des domaines autorisés, ajouter `api.chess.com`. Avec un abonnement individuel payant, chacun le fait lui-même; avec un abonnement Team ou Enterprise, c'est l'administrateur qui le fait (Paramètres de l'organisation, Capacités); avec l'offre gratuite, ce n'est pas possible. Sans ce réglage, on colle simplement le PGN de chaque partie.
5. Dans une nouvelle conversation, écrire "Initialise mon profil". Claude crée les fiches joueur/ et pose quelques questions (niveau, classement, plateforme, notation, objectifs, fork éventuel du dépôt).

## Utilisation
- **Jouer une partie**: ouvrir une nouvelle conversation dans le projet pour chaque partie. Claude demande la couleur (ou un tirage au sort), l'ouverture éventuelle et le thème éventuel.
- **Analyser une partie chess.com**: demander par exemple "Analyse ma dernière partie", "ma partie contre tel adversaire", "liste mes 10 dernières parties", ou donner le lien de la partie. Claude la récupère avec le pseudo du profil (domaine api.chess.com à autoriser, voir plus haut), avec la pendule et la vraie fin de partie.
- **Analyser une autre partie**: coller le PGN (sur chess.com ou Lichess, bouton de partage puis PGN). Plusieurs PGN peuvent être envoyés dans la même conversation.
- **Variantes**: désactivées par défaut. Les demander juste après avoir vu la page, dans la même conversation: Claude les ajoute en une étape. Dans une autre conversation, il faudrait refaire l'analyse.
- **Suivi**: après chaque partie ou analyse, Claude met à jour les fiches joueur/. On peut les relire et les corriger à tout moment. L'index des parties ne garde que le mois en cours; les mois passés sont archivés dans joueur/historique-AAAA-MM.md.

## Mettre à jour les règles
- **Avec GitHub**: synchroniser son fork si on en a un ("Sync fork"), puis demander "Mets à jour les règles depuis le dépôt".
- **Sans GitHub**: télécharger le nouveau ZIP et demander à Claude de réenregistrer les documents claude/instructions.md, regles/, outils/ et modeles/.

Dans les deux cas, les fiches joueur/ ne sont pas touchées.

## Contribuer
Les améliorations des règles et des outils sont les bienvenues, par issue ou pull request. Tout passe par une pull request: personne ne commite directement sur main, la branche est protégée.

Pendant les parties et les analyses, Claude ne modifie pas les règles: s'il repère une amélioration, il la propose. Pour la soumettre:
1. Avoir forké le dépôt et relié GitHub à claude.ai.
2. Demander explicitement, par exemple "Propose cette règle au dépôt, dans regles/partie.md".
3. Claude clone le fork, crée une branche, fait le commit, la pousse et ouvre la pull request vers ce dépôt. Il met aussi à jour le document correspondant dans le projet.
4. Vérifier avant l'envoi que la modification ne contient aucune donnée personnelle (parties, pseudo, classement): ces informations restent dans joueur/.

Utilisateurs de Claude Code: le fichier CLAUDE.md permet de travailler directement dans un clone local. Les fiches joueur/ vivent alors dans le dossier joueur/ du clone, exclu des commits par le .gitignore.

## Remarques
- Les pages d'analyse demandent que la session de Claude puisse installer des paquets Python et cloner ou télécharger depuis GitHub (ce dépôt, Stockfish, la base d'ouvertures). Sans GitHub, Claude analyse quand même la partie, mais sans moteur, et doit le préciser. Sans la base d'ouvertures, la page n'affiche pas le nom de l'ouverture.
- Coût: une analyse est organisée pour limiter les échanges avec les outils (chaque échange relit toute la conversation), et ne comporte des variantes que sur demande. Une partie simple peut aussi être commentée directement dans la conversation, sans page.
- Pièces de l'échiquier: jeu cburnett de Colin M.L. Burnett. Moteur: Stockfish.

## Licence
Ce dépôt est distribué sous licence MIT (voir le fichier LICENSE).

Les outils téléchargés à l'installation gardent leur propre licence et ne font pas partie du dépôt: python-chess et Stockfish (GPL-3.0), et la base d'ouvertures chess-openings de lichess (licence dans son fichier COPYING.txt). Les pièces cburnett, générées depuis python-chess au moment de construire une page d'analyse, restent sous la licence de leur auteur.
