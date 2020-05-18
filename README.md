# Maze Solver
I love visualizing algorithms so I built this portfolio project showing how different pathfinding algorithms solve a maze. Though the program launches with a starting maze the user can draw any maze they like to challenge the algorithms. All algorithms in this project are allowed to move diagonally.

![Main Screen](/images/main_screen.PNG)

## The Pathfinders
**Random Backtracking**
This algorithm is to serve as a kind of baseline as it is the most inefficent and "dumb" algorithm in the project. Does not know where the exit is and moves around randomly searching for it but if it runs into a deadend or itself uses recursive backtracking to randomly choose another direction that has not yet been checked. Since this algorithm is random there is a theoretical chance it could find the shortest path to the exit.... its just very very unlikely to do so.

**Breadth-First Search**
Operates on a queued first in, first out (FIFO) method of searching through the maze. This means the search propagates outward similar to a flood filling the maze as it searches for the exit. BfS works best in a maze when the exit location is not known and the distance between maze cells is constant or unweighted. Will find the shortest path to the exit though the more maze cells that need to be checked the slower and less efficiant this algorithm becomes.

**A***
The star amongst the algorithms in this project (pun intended) is the A* algorithm. Finds the shortest path like breadth-first search but finds it in the most efficiant and fastest way. The only draw back of A* is that it needs to know the location of the exit to function. A* operates by scoring maze cells using a combination of their cell to cell distance for the starting cell and the straight line distance to the exit cell. Then it chooses which cells to check next based off the best scores. This means A* searches intelligently prioritizing the cells with the best chance at being closer to the end while not being to far from the start. Once the exit is reached the best and shortest path is found by following the best scoring cells from the exit back to the start.
