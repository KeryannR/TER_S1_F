# TER_S1_F: member Arno LESAGE


### First session:
#### Papers read:
- K. Cheng, H. Liu, and X. Dou, “Randomized pacman maze generation algorithm,” Applied and Computational Engineering, vol. 42, pp. 156–162, Feb. 2024. doi: 10.54254/2755-2721/42/20230771. [Online]. Available: https://www.researchgate.net/publication/382389091_Randomized_Pacman_maze_generation_algorithm -> réduire le nombre de deadend
- Mazes for Programmers Code Your Own Twisty Little Passages (Jamis Buck), Chapiter 5: Hund & Kill, Counting Dead Ends, Chapter 9: Braiding Mazes
- https://www.astrolog.org/labyrnth/algrithm.htm (Info supplémentaire sur les charactéristique des algorithmes)

#### Remarks:
Il manque d'espaces innacessible aux joueurs, il faut inspecter le biais vers les bords.
Voir l'algo tetris:
https://shaunlebron.github.io/pacman-mazegen/
#### Implementation:
- Implementation of the Hunt & Kill algorithm, the choice was motivated by aesthetic criteria
- Implementation of a braided version of the Hunt & Kill algorithm to make mazes where some isolated blocks may occurs **(check bias)**
- Implementation of the Grid and Cell classes 

### Second session:
#### Documentation read:
- https://shaunlebron.github.io/pacman-mazegen/

#### Remarks:
- La version Tetris de la génération de labyrinthe pacman par Shaun Le Bron se révèle beaucoup trop complexe, l'algorithme n'est pas donné, la documentation ne dit pas grand chose et le code (~2000 lignes) est beacuoup trop long pour être compris de manière simple. Il a donc été décidé d'implémenter une version modifié afin de gagner du temps. 
- Il manque toujours d'espaces inaccessibles aux joueurs,
- Le nouvel algorithme n'a plus de biais visible
- ~~Il faut implémenter un moyen de réduire les "spikes" sur les bords de la grille qui engendrent des culs de sacs~~ [done]
- Il faut implémenter un moyen de retirer les chemein de 2 de large
- Il faut rajouter la boite au fantômes 

#### Implementation:
- Implémentation d'une version modifié de l'algorithme basé sur Tetris. Dans le nouvel algorithme, des cellules sont créés et placés aléatoirement sur la grille. Le résultat est sensuite mis en mirroir et concaténé en symmetrie par les deux axes.

### Third session:
#### Implementation:
- Implémentation d'un wrapper pour l'appel du fichier de génration de Maze à partir du terminal avec des paramètres (permettra de simplifier l'implémentation finale de l'API).
- Retrait d'un bug engendrant de la 8-connexité lorsqu'une symétrie était impliquée ou que l'on retirait les border spikes (voir séance 2).
- Début de l'implémentation de pièces large pour plus ressembler à PACMAN... \[spoiler: marche pas vraiment\]

### Fourth session:
#### Implementation:
- Implémentation d'une fonction de score pour l'évaluation automatique de labyrinthe PACMAN. Ce score se base sur les mériques calculés précédemment (proportion de cul-de-sac, chemin droit, carrefour, virage, jonctions) et les compare avec un cosinus de similarité sur ces mêmes métriques calculés sur plusieurs labyrinthes pacman rééls.
- Refactorisation du GitHub

### Fifth session:
#### Implementation:
- Finalisation de la métrique du cosinus de similarité avec des seuils pour faire un map vers les entiers de 0 à 5,
- Mise en place de la boite aux fantômes et des téléporteurs
-  LaTeX Beamer

### Before Sixth session:
#### Implementation:
- Mise en place de la possibilité d'écraser des pièces lors de la génération du labyrinthes (ne le fait pas par défaut et est lié à une probabilité).
- Mise à jour de la métrique d'évaluation des labyrinthes pour éliminer les labyrinthes ayant trop de carrefours, de chemin ou de murs.
- Ajout à la métrique d'évaluation de poids (possiblement optimisable) pour accorder plus ou moins d'importance à la ressemblance pour une métrique données.