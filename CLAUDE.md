# Echecs avec Claude

Lire instructions.md et suivre ses règles. Les procédures occasionnelles (initialisation, mise à jour des règles, contribution) sont dans procedures.md.

## Emplacement des fiches du joueur (joueur/)
- Si la conversation est rattachée à un projet claude.ai, ce sont des documents du projet. Le clone sert à récupérer les outils d'analyse, importer, mettre à jour ou contribuer.
- Sinon (Claude Code dans un clone local), c'est le dossier joueur/ du clone, exclu du dépôt par le .gitignore. Les fichiers d'une analyse (partie.json, analyse.json, complement.json, page.html, fiche.md, index.txt) sont produits dans un dossier hors du clone.

## Modifications du dépôt
- Ne jamais commiter sur main: créer une branche depuis main, pousser la branche, ouvrir une pull request vers main. Une pull request par sujet, jamais basée sur une autre branche de travail.
- Tester le script avant de le proposer (analyser, verifier, build sur une partie).
- Ne jamais ajouter de données du joueur à un commit (parties, pseudo, classement, fichiers d'analyse).
- Ne modifier les documents communs que sur demande explicite du joueur. Mettre à jour le README quand l'installation, l'utilisation ou le coût changent.
