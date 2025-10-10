# TER_S1_F

### First session:
#### Papers read:
- "Maze Classification" by Walter D. Pullen : https://www.astrolog.org/labyrnth/algrithm.htm
- "Pac-Man Maze Generation" by Shaun LeBron : https://shaunlebron.github.io/pacman-mazegen/
- "Mazes for Programmers Code Your Own Twisty Little Passages" by Jamis Buck : http://mazesforprogrammers.com/

#### Research:
- Explored the structure of existing maze generation algorithms (Hunt-and-Kill and Tetris).

#### Implementations:
- Created a GitHub repository to host the project and organize files.
- Set up the initial project structure

### Second session: 
#### Papers read:
- "An extensive comparative analysis on different maze generation algorithms" by D. Mane : https://ijisae.org/index.php/IJISAE/article/view/3557/2162

#### Research:
- Studied metrics to describe maze structures, focusing on local connectivity (Dead-Ends, Straights, Turns, Junctions, Crossroads).
- Analyzed how Tetris-based maze generation differs structurally from Hunt-and-Kill.

### Implementations:
- Moved metrics computation into a separate metrics package.
- Tested metrics on sample mazes generated with Hunt-and-Kill and Tetris-based approaches.
- Firt implementation of metrics on Hunt-and-Kill mazes.
- Implemented functions to calculate Dead-Ends%, Straights%, Turns%, Junctions%, Crossroads% for any maze represented as a 2D NumPy array.