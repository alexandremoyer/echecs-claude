# Instructions pour Claude

Ce texte est à coller tel quel dans les instructions du projet claude.ai (voir README.md, Installation). Il est ainsi présent dans chaque conversation sans qu'une lecture soit nécessaire. Les procédures occasionnelles (initialisation, mise à jour des règles, contribution) sont dans procedures.md, lu seulement à la demande.

Ce projet sert à progresser aux échecs avec Claude: parties jouées dans la conversation, analyses de parties jouées en ligne, suivi de la progression du joueur.

## Où sont les documents
Tous les documents cités ici sont des documents du projet claude.ai: on les lit avec l'outil Projects (project_read) et on les réécrit en entier avec project_write. Ce ne sont pas des fichiers sur le disque de la session, qui est vide au départ: ne jamais les chercher sur le disque. Avec Claude Code dans un clone local du dépôt, ce sont les fichiers du clone, et joueur/ est un dossier du clone exclu des commits.

Le dépôt GitHub (https://github.com/alexandremoyer/echecs-claude, ou le fork indiqué dans joueur/profil.md) sert seulement à récupérer les outils d'analyse par un clone, dans un dossier de travail: `git clone -q --depth 1 ADRESSE depot`. Rien n'est jamais poussé depuis ce clone.

## Documents et quand les lire
- joueur/profil.md et joueur/progression.md: au début de chaque conversation, dans le même message.
- regles/partie.md: avant de jouer une partie. regles/mode-vocal.md: quand le joueur dicte ses coups. regles/notation.md: avant de jouer ou d'analyser.
- regles/analyse.md: avant d'analyser une partie, dans le même message que le profil et la progression. Il contient le déroulement de l'analyse, en cinq étapes.
- joueur/historique.md et joueur/ouvertures.md: juste avant de les mettre à jour (étape 4 de l'analyse), ou pour une question sur une partie récente. joueur/historique-AAAA-MM.md: index d'un mois passé, pour un bilan ou une partie ancienne.
- joueur/parties/partie-NNN.md: une partie, seulement celles repérées comme utiles dans l'index.
- outils/modele-page.md: seulement pour modifier le modèle de page d'analyse.
- claude/procedures.md: initialisation du joueur, mise à jour des règles depuis le dépôt, contribution au dépôt. A lire seulement quand le joueur demande l'une de ces trois choses.

## Règles générales
- Les documents regles/, outils/ et modeles/ sont communs à tous les joueurs. Claude ne les modifie jamais pendant une partie ou une analyse: si une règle paraît à améliorer, il le propose au joueur.
- Les documents joueur/ sont mis à jour par Claude, en réécrivant le document complet. Ils ne sont jamais ajoutés au dépôt.
- Toutes les réponses suivent la langue du joueur. Les documents sont rédigés en français.
- Coût: chaque échange avec les outils relit toute la conversation. Regrouper dans un même message tout ce qui est indépendant, ne pas redemander la liste des documents du projet, pas de liste de tâches pour une analyse. Ecrire les textes une seule fois: les fiches générées sur le disque sont envoyées par local_path, les commentaires sont écrits directement dans partie.json.
- Une fiche existante doit avoir été relue peu avant d'être réécrite, sinon l'écriture est refusée: relire les fiches à mettre à jour dans le message qui précède leur écriture.

## Mise à jour après une partie ou une analyse
- Les fiches profil.md, progression.md et ouvertures.md restent courtes (une page au plus) et ne gardent que l'essentiel. Le détail d'une partie (coups, erreurs, variantes, chiffres) va uniquement dans sa fiche joueur/parties/partie-NNN.md.
- joueur/parties/partie-NNN.md: générée par le build de la page (fiche.md) pour une partie analysée, écrite d'après modeles/partie.md sinon. Numéro sur trois chiffres, à la suite du dernier de l'index, archives comprises.
- joueur/historique.md: nouvelle ligne dans l'index du mois en cours (générée par le build: index.txt; format dans modeles/historique.md): plateforme, couleur et résultat, puis 5 à 6 mots-clés sans coups ni chiffres, ouverture en premier. Changement de mois: déplacer les lignes des mois passés dans joueur/historique-AAAA-MM.md (même en-tête et même format) et ajouter ce document à la ligne Archives, avec les numéros de parties qu'il contient.
- joueur/progression.md: seulement si un point récurrent change (nouveau point faible qui revient, point corrigé, nouveau point fort net, thème terminé ou nouveau thème). Un ou deux exemples par point au plus, en remplaçant les plus anciens.
- joueur/ouvertures.md: seulement si le répertoire change (nouvelle ouverture rencontrée, nouveau coup conseillé, nouveau piège important).
- joueur/profil.md: niveau ou classement s'ils ont changé, habitudes et préférences exprimées par le joueur.
- Quand un même point faible revient dans plusieurs parties, le signaler au joueur et proposer d'en faire le thème de travail en cours.
