# Analyse d'une partie

S'applique aux parties jouées avec Claude comme aux parties jouées en ligne (récupérées avec le pseudo du joueur, ou PGN collé). Le détail des commandes et des champs est dans outils/rendu-analyse.md: ce document suffit pour une analyse courante.

## Déroulement en cinq étapes
Chaque étape de la conversation (un aller-retour entre Claude et ses outils) relit tout ce qui précède: le coût d'une analyse dépend surtout du nombre d'étapes. Une analyse tient en cinq étapes. Pas de liste de tâches, pas de script de vérification écrit à la main, pas de lecture du format: tout ce qu'il faut est affiché par les commandes.
1. Lectures, dans un seul message et rien d'autre: joueur/profil.md, joueur/progression.md, regles/analyse.md, regles/notation.md. Ne pas redemander la liste des documents du projet.
2. Une seule commande, au premier plan, timeout 120 secondes:
   `mkdir -p travail && cd travail && git clone -q --depth 1 ADRESSE depot; cp depot/outils/modele-analyse.html depot/outils/outils-analyse.py . && python3 -u outils-analyse.py analyser PSEUDO CHOIX`
   (dossier travail dans le dossier courant de la session, jamais dans ~: les fichiers envoyés au projet par local_path doivent être sous le dossier courant)
   (ADRESSE: dépôt du profil; ajouter --lichess pour lichess; CHOIX: rang dans la liste des dernières parties, pseudo de l'adversaire ou lien de la partie). PGN collé par le joueur: écrire le PGN dans un fichier dans la même commande (`cat > partie.pgn <<'EOF' ... EOF`) puis `python3 -u outils-analyse.py analyser PSEUDO --pgn partie.pgn` (PSEUDO ou "noirs" donne la couleur du joueur). La commande installe les outils si besoin et affiche tout ce qu'il faut pour rédiger: infos, pendule, analyse coup par coup avec les mats en clair, indicateur de triche, étiquettes automatiques, mats manqués, ouvertures, et le squelette des champs à rédiger.
3. Seulement si une affirmation reste douteuse: une seule commande `python3 -u outils-analyse.py verifier partie.json SPEC...`, avec toutes les positions à vérifier (SPEC: coup de la partie pour la position avant ce coup, +coup pour la position après, :c1,c2 pour évaluer des coups précis). Ne pas écrire de script de vérification.
4. Dans un seul message: la commande `cat > complement.json <<'EOF' ... EOF && python3 outils-analyse.py build partie.json analyse.json modele-analyse.html page.html` (complement.json: numero, titre, entete, commentaires, bilan, lecons, mots_cles, remarques si besoin; le build complète les champs absents et écrit la page, la fiche fiche.md et la ligne d'index index.txt), et, dans le même message, les lectures de toutes les fiches qui seront réécrites à l'étape 5: joueur/historique.md, joueur/ouvertures.md, joueur/progression.md, et joueur/profil.md si elle change (une fiche lue trop longtemps avant son écriture est refusée). Relire ses commentaires avant d'envoyer, pour ne pas reconstruire la page.
5. Dans un seul message: envoi de page.html au joueur (SendUserFile, affichage inline; publication en artifact seulement si le joueur la demande), écriture de joueur/parties/partie-NNN.md par local_path depuis fiche.md, réécriture de joueur/historique.md avec la ligne d'index ajoutée (et archivage du mois précédent si le mois a changé), puis progression.md, ouvertures.md et profil.md seulement si elles changent. Ensuite la réponse au joueur, qui se termine par une ligne "Titre pour cette conversation: Partie N, <titre de la page>", pour que le joueur renomme la conversation.

Variantes demandées après coup, dans la même conversation: les ajouter dans complement.json, relancer build et renvoyer la page, en une seule étape. Dans une autre conversation, il faut refaire l'analyse.

## Parties chess.com et lichess
- Si le joueur ne donne pas de PGN, récupérer la partie avec son pseudo (pseudos dans joueur/profil.md). Sans précision du joueur, prendre sa plateforme principale. Si le domaine (api.chess.com ou lichess.org) est inaccessible, demander le PGN.
- Quand la pendule est connue, la commenter: temps restant, coups joués trop vite ou trop lentement, erreurs jouées en quelques secondes. Le bilan dit si la pendule a joué un rôle.

## Plusieurs parties envoyées d'un coup
D'abord un tri rapide au moteur (résultat, coup qui fait basculer chaque partie, lien avec le thème en cours), puis une page d'analyse par partie, chacune selon le déroulement ci-dessus.

## Vérification
- Toute affirmation sur la partie vient de la sortie du moteur (commandes analyser et verifier): ne rien affirmer de tête, y compris les mats, les clouages et les pièces qui défendent une case.
- Si le moteur n'est pas disponible, le dire clairement et présenter l'analyse comme faite de tête.
- Honnêteté sur les erreurs de Claude aussi, pendant la partie comme dans l'analyse.

## Contenu
- Etiquette pour chaque coup (excellent, bon, imprécis, erreur, gaffe), calculée automatiquement d'après la perte mesurée par le moteur, et corrigée à la main si besoin ("tag" dans le commentaire). "Excellent" est toujours donné à la main.
- Calcul: perte jusqu'à 0,5 point, bon; jusqu'à 1 point, imprécis; jusqu'à 2,5 points, erreur, ou imprécis si la position reste presque égale (moins d'un point d'écart); plus de 2,5 points, gaffe, ou erreur si le camp qui joue reste nettement mieux (1,5 point ou plus). Avec un gros avantage (5 points ou plus après le coup), un mat raté ou une perte est noté imprécis; avec un gros retard (5 points ou plus avant le coup), une perte jusqu'à 2,5 points aussi.
- Commentaire seulement pour les coups qui comptent, une douzaine au plus: erreurs et gaffes, coups excellents ou marquants, tournants de la partie, coups d'ouverture (le coup qui définit l'ouverture, les changements de variante, la sortie de la théorie), y compris les coups de Claude dans une partie jouée avec lui. Les autres coups gardent la traduction en clair et la ligne du meilleur coup, sans commentaire.
- Quand un coup est une erreur, proposer la meilleure alternative et l'expliquer.
- Ouverture: le nom de l'ouverture et de la variante est reconnu automatiquement par position (base d'ouvertures lichess) et affiché sur chaque coup de la théorie. Les noms de la base sont en partie en anglais: les traduire dans les commentaires.
- Répondre à chaque remarque faite par le joueur pendant la partie, en citant la remarque ("remarques", et une leçon "Remarque du joueur").
- Variantes expliquées (lignes à rejouer coup par coup): désactivées par défaut, seulement si le joueur les demande.
- Bilan en fin de page: points positifs, points à retenir, une leçon clé. Indicateur de triche des deux camps, présenté comme une information et jamais comme une probabilité.
- Fiche de la partie: "lecons" (coups clés avec symbole, explication courte et meilleure alternative; remarque du joueur et réponse; points positifs) et "mots_cles" (5 à 6, ouverture en premier, sans coups ni chiffres). La pendule, l'indicateur et les mats manqués sont ajoutés automatiquement.

## Forme
- Page d'analyse interactive, construite par le script (modèle décrit dans outils/modele-page.md).
- Explications simples et concrètes, sans théorie inutile, en nommant les pièces et les cases. Tutoiement ou vouvoiement selon joueur/profil.md.
- Echiquier retourné quand le joueur a les Noirs (automatique pour une partie récupérée).
