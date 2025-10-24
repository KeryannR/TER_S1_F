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

### Third session
#### Papers read:
None this session — the focus was on testing and validation of the existing codebase.

#### Research:
- Studied unit testing strategies for procedural content generation systems (maze generators).
- Investigated how to validate maze structures through topological properties (connectivity, symmetry, wall density).

#### Implementations:
- This testing phase serves as the foundation for upcoming API development.
- Designed and implemented a complete unit testing suite using Python’s unittest framework.
- Structured the test suite into two main sections:
  - Basic functionality tests: verifying maze size, JSON output structure, fixed seeds, and grid validity.
  - Advanced robustness tests: checking symmetry, maze connectivity (flood-fill), wall density, invalid parameter handling, and performance.
- Added skip conditions for optional features (e.g., missing tile files) to ensure smooth CI/CD integration.
- Improved test readability with descriptive comments.
- Verified maze generation consistency across multiple seeds and configuration parameters.
- Confirmed full JSON compatibility for API deployment.


### Fourth session
#### Research:
- Studied how to test Flask APIs using unittest and Flask’s test client.
- Investigated CI/CD strategies for Python projects on GitHub, including automated test execution on push/pull requests.

#### Implementations:
- Developed a dedicated test suite (tests/test_mazeAPI.py) for the Flask API to: Test default maze generation, Test reproducibility with a fixed seed...
- Ensured skipped tests for optional resources to allow smooth CI/CD execution.
- Verified that the API responses are consistent, correct, and JSON-serializable.
- Researched and prepared steps to integrate CI/CD using GitHub Actions, including setting up automated test runs on push or pull requests.

