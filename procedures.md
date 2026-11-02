# Procédures occasionnelles

Dans un projet claude.ai, ce document est enregistré sous claude/procedures.md. Il n'est lu que sur demande du joueur, pour l'une des trois procédures ci-dessous. Les règles du quotidien sont dans instructions.md, collé dans les instructions du projet.

## Initialisation (première conversation)
Si les documents joueur/ n'existent pas encore:
1. Créer joueur/profil.md, joueur/progression.md, joueur/ouvertures.md et joueur/historique.md à partir des modèles du dossier modeles/. Les fiches joueur/parties/ seront créées partie après partie.
2. Poser au joueur, une par une, les questions qui correspondent aux zones [A COMPLETER] de joueur/profil.md, et remplir le document. Parmi elles: le joueur a-t-il un fork du dépôt? Si oui, noter son adresse; sinon, noter "dépôt d'origine". Demander aussi s'il préfère le tutoiement ou le vouvoiement.
3. Ne rien inventer: une information inconnue reste vide et se complète au fil des parties.

## Mise à jour des règles depuis le dépôt
Sur demande du joueur ("Mets à jour les règles depuis le dépôt"):
1. Cloner le dépôt du joueur (dépôt d'origine, ou fork indiqué dans joueur/profil.md).
2. Comparer avec les documents du projet et résumer au joueur ce qui change.
3. Réécrire dans le projet les documents regles/, outils/ et modeles/, au même chemin, et procedures.md sous claude/procedures.md. Supprimer ceux qui n'existent plus dans le dépôt. Le modèle de page, le script et l'exemple (outils/modele-analyse.html, outils/outils-analyse.py, outils/exemple-partie.json) ne sont pas copiés dans le projet: ils viennent du clone à chaque analyse.
4. Si instructions.md a changé, donner au joueur son nouveau contenu en texte brut, à coller dans les instructions du projet: Claude ne peut pas modifier les instructions du projet lui-même.
5. Ne jamais toucher aux documents joueur/. Si un modèle a changé (nouvelle section), proposer d'ajouter la section correspondante dans la fiche du joueur.

## Contribution au dépôt
Sur demande explicite du joueur ("Propose cette modification au dépôt"):
1. Cloner le fork du joueur et le mettre à jour depuis le dépôt d'origine.
2. Créer une branche au nom explicite, depuis main. Ne jamais commiter sur main. Une pull request par sujet, toujours vers main: pas de pull request dont la base est une autre branche de travail.
3. Appliquer la modification, la tester (pour le script: analyser, verifier et build sur une partie), montrer le résultat au joueur, puis faire le commit.
4. Vérifier que le commit ne contient aucune donnée personnelle (parties, pseudo, classement, fichiers d'analyse).
5. Pousser la branche et ouvrir la pull request vers le dépôt d'origine, avec une description claire de la modification et de sa raison. Mettre à jour le README si l'installation, l'utilisation ou le coût changent.
6. Mettre à jour le document correspondant dans le projet.
