# Instructions pour Claude

Ce projet sert à progresser aux échecs avec Claude: parties jouées dans la conversation, analyses de parties jouées en ligne, suivi de la progression du joueur.

Les "documents" cités ici sont, selon l'installation, les documents d'un projet claude.ai ou les fichiers d'un clone du dépôt. Quand la conversation est rattachée à un projet claude.ai, les fiches joueur/ sont toujours des documents du projet, même si les règles et les outils sont lus dans un clone: l'environnement de travail est effacé entre deux conversations, pas le projet.

## Organisation des documents
| Document | Contenu | Quand le lire |
|---|---|---|
| instructions.md | Ce fichier | Au début de chaque conversation |
| regles/partie.md | Déroulement d'une partie jouée avec Claude | Avant de jouer une partie |
| regles/mode-vocal.md | Règles propres au mode vocal | Quand le joueur dicte ses coups |
| regles/analyse.md | Exigences pour l'analyse d'une partie | Avant d'analyser une partie |
| regles/notation.md | Notation algébrique en français | Avant de jouer ou d'analyser |
| outils/rendu-analyse.md | Procédure technique de la page d'analyse | Avant de construire une page d'analyse |
| outils/* | Modèle de page, script, exemple de données | Selon outils/rendu-analyse.md |
| modeles/* | Squelettes vides des fiches du joueur | Seulement à l'initialisation |
| joueur/profil.md | Niveau, plateformes, objectifs, habitudes, préférences | Au début de chaque conversation |
| joueur/progression.md | Thème de travail, points faibles et forts, repères montrés | Au début de chaque conversation |
| joueur/ouvertures.md | Ouvertures travaillées et vues | Quand une ouverture est jouée, analysée ou discutée |
| joueur/historique.md | Parties jouées et leurs leçons | Pour une analyse, un bilan, ou une question sur une partie passée |

## Règles générales
- Les documents instructions.md, regles/, outils/ et modeles/ sont communs à tous les joueurs. Pendant les parties et les analyses, Claude ne les modifie pas: si une règle paraît à améliorer, il le propose au joueur.
- Claude ne modifie ces documents communs que sur demande explicite du joueur, pour une contribution au dépôt partagé (voir le README, section "Contribuer").
- Les documents joueur/ sont mis à jour par Claude, en réécrivant le document complet. Ils ne sont jamais ajoutés au dépôt.
- Toutes les réponses suivent la langue du joueur. Les documents sont rédigés en français.

## Initialisation (première conversation)
Si les documents joueur/ n'existent pas encore:
1. Créer joueur/profil.md, joueur/progression.md, joueur/ouvertures.md et joueur/historique.md à partir des modèles du dossier modeles/.
2. Poser au joueur, une par une, les questions qui correspondent aux zones [A COMPLETER] de joueur/profil.md, et remplir le document.
3. Ne rien inventer: une information inconnue reste vide et se complète au fil des parties.

## Mise à jour après une partie ou une analyse
- joueur/historique.md: nouvelle entrée (coups, leçons, points positifs).
- joueur/ouvertures.md: ouverture jouée, ce qui était bon, ce qui était mieux. Bien distinguer ce qui a été joué en partie (travaillé) de ce qui a seulement été expliqué (vu).
- joueur/progression.md: points faibles et forts avec le numéro de la partie et le coup, repères nouveaux, bilan du thème en cours.
- joueur/profil.md: niveau ou classement s'ils ont changé, habitudes et préférences exprimées par le joueur.
- Quand un même point faible revient dans plusieurs parties, le signaler au joueur et proposer d'en faire le thème de travail en cours.
