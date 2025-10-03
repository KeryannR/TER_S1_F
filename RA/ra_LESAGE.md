# TER_S1_F: member Arno LESAGE


### First session:
#### Papers read:
- K. Cheng, H. Liu, and X. Dou, “Randomized pacman maze generation algorithm,” Applied and Computational Engineering, vol. 42, pp. 156–162, Feb. 2024. doi: 10.54254/2755-2721/42/20230771. [Online]. Available: https://www.researchgate.net/publication/382389091_Randomized_Pacman_maze_generation_algorithm -> réduire le nombre de deadend
- Mazes for Programmers Code Your Own Twisty Little Passages (Jamis Buck), Chapiter 5: Hund & Kill, Counting Dead Ends, Chapter 9: Braiding Mazes
- https://www.astrolog.org/labyrnth/algrithm.htm (Info supplémentaire sur les charactéristique des algorithmes)

#### Remarks:
Il manque d'espaces innacessible aux joueurs, il faut inspecter le biais vers les bords.
#### Implementation:
- Implementation of the Hunt & Kill algorithm, the choice was motivated by aesthetic criteria
- Implementation of a braided version of the Hunt & Kill algorithm to make mazes where some isolated blocks may occurs **(check bias)**
- Implementation of the Grid and Cell classes 
