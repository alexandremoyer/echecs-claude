# Instructions pour Claude

Ce projet sert à progresser aux échecs avec Claude: parties jouées dans la conversation, analyses de parties jouées en ligne, suivi de la progression du joueur.

Les "documents" cités ici sont les documents du projet claude.ai (ou, avec Claude Code, les fichiers d'un clone local du dépôt). Les règles et les fiches du joueur sont lues dans les documents du projet. Le dépôt GitHub sert à récupérer les outils d'analyse sans les recopier, à mettre à jour les règles et à proposer une modification (voir plus bas).

## Dépôt GitHub
- Dépôt d'origine: https://github.com/alexandremoyer/echecs-claude
- Si joueur/profil.md indique un autre dépôt (fork du joueur), utiliser celui-là. Sinon, utiliser le dépôt d'origine.
- Clone pour lire les outils: `git clone -q --depth 1 <adresse> depot`, dans un dossier de travail. Rien n'est jamais poussé depuis ce clone.

## Organisation des documents
| Document | Contenu | Quand le lire |
|---|---|---|
| instructions.md (claude/instructions.md dans un projet claude.ai) | Ce fichier | Au début de chaque conversation |
| regles/partie.md | Déroulement d'une partie jouée avec Claude | Avant de jouer une partie |
| regles/mode-vocal.md | Règles propres au mode vocal | Quand le joueur dicte ses coups |
| regles/analyse.md | Exigences pour l'analyse d'une partie | Avant d'analyser une partie |
| regles/notation.md | Notation algébrique en français | Avant de jouer ou d'analyser |
| outils/rendu-analyse.md | Procédure technique de la page d'analyse | Avant de construire une page d'analyse |
| outils/* | Modèle de page, script, exemple de données | Pris dans un clone du dépôt, selon outils/rendu-analyse.md |
| modeles/* | Squelettes vides des fiches du joueur | Seulement à l'initialisation |
| joueur/profil.md | Niveau, plateformes, objectifs, habitudes, préférences, dépôt | Au début de chaque conversation |
| joueur/progression.md | Thème de travail, points faibles et forts, repères montrés | Au début de chaque conversation |
| joueur/ouvertures.md | Ouvertures travaillées et vues | Quand une ouverture est jouée, analysée ou discutée |
| joueur/historique.md | Index des parties: une ligne par partie, avec des mots-clés | Pour une analyse, un bilan, ou une question sur une partie passée |
| joueur/parties/partie-NNN.md | Une partie: coups, leçons, remarques du joueur | Seulement les parties utiles, repérées dans l'index |

## Règles générales
- Les documents instructions.md, regles/, outils/ et modeles/ sont communs à tous les joueurs. Pendant les parties et les analyses, Claude ne les modifie pas: si une règle paraît à améliorer, il le propose au joueur.
- Claude ne modifie ces documents communs que sur demande explicite du joueur: mise à jour depuis le dépôt, ou contribution.
- Les documents joueur/ sont mis à jour par Claude, en réécrivant le document complet. Ils ne sont jamais ajoutés au dépôt.
- Toutes les réponses suivent la langue du joueur. Les documents sont rédigés en français.

## Initialisation (première conversation)
Si les documents joueur/ n'existent pas encore:
1. Créer joueur/profil.md, joueur/progression.md, joueur/ouvertures.md et joueur/historique.md à partir des modèles du dossier modeles/. Les fiches joueur/parties/ seront créées partie après partie, à partir de modeles/partie.md.
2. Poser au joueur, une par une, les questions qui correspondent aux zones [A COMPLETER] de joueur/profil.md, et remplir le document. Parmi elles: le joueur a-t-il un fork du dépôt? Si oui, noter son adresse; sinon, noter "dépôt d'origine".
3. Ne rien inventer: une information inconnue reste vide et se complète au fil des parties.

## Mise à jour après une partie ou une analyse
Principe: les fiches profil.md, progression.md et ouvertures.md restent courtes (une page chacune au plus) et ne gardent que l'essentiel. Le détail d'une partie (coups, erreurs, variantes, chiffres) va uniquement dans sa fiche joueur/parties/partie-NNN.md.
- joueur/parties/partie-NNN.md: nouvelle fiche à partir de modeles/partie.md (coups, leçons, remarques du joueur, points positifs). Numéro sur trois chiffres, à la suite du dernier de l'index.
- joueur/historique.md: nouvelle ligne dans l'index, avec 5 à 8 mots-clés choisis pour retrouver la partie plus tard (ouverture, thèmes tactiques, erreurs et réussites marquantes). Si une partie déjà indexée est complétée, mettre aussi sa ligne à jour.
- joueur/progression.md: mise à jour seulement si un point récurrent change (nouveau point faible qui revient, point corrigé, nouveau point fort net, thème terminé ou nouveau thème). Un ou deux exemples par point au plus, en remplaçant les plus anciens.
- joueur/ouvertures.md: mise à jour seulement si le répertoire change (nouvelle ouverture rencontrée, nouveau coup conseillé, nouveau piège important). Pas de compte rendu partie par partie.
- joueur/profil.md: niveau ou classement s'ils ont changé, habitudes et préférences exprimées par le joueur.
- Quand un même point faible revient dans plusieurs parties, le signaler au joueur et proposer d'en faire le thème de travail en cours.

## Mise à jour des règles depuis le dépôt
Sur demande du joueur ("Mets à jour les règles depuis le dépôt"):
1. Cloner le dépôt du joueur (voir la section Dépôt GitHub).
2. Comparer avec les documents du projet et résumer au joueur ce qui change.
3. Réécrire dans le projet instructions.md (sous claude/instructions.md) et les documents regles/, outils/ et modeles/, au même chemin. Supprimer ceux qui n'existent plus dans le dépôt.
4. Ne jamais toucher aux documents joueur/. Si un modèle a changé (nouvelle section), proposer d'ajouter la section correspondante dans la fiche du joueur.

## Contribution au dépôt
Sur demande explicite du joueur ("Propose cette modification au dépôt"):
1. Cloner le fork du joueur et le mettre à jour depuis le dépôt d'origine.
2. Créer une branche au nom explicite. Ne jamais commiter sur main.
3. Appliquer la modification, montrer le résultat au joueur, puis faire le commit.
4. Vérifier que le commit ne contient aucune donnée personnelle (parties, pseudo, classement, fichiers d'analyse).
5. Pousser la branche et ouvrir la pull request vers le dépôt d'origine, avec une description claire de la modification et de sa raison.
6. Mettre à jour le document correspondant dans le projet.
