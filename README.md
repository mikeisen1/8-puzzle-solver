# 8-puzzle solver

This project solves a given 8-puzzle to one of four possible 8-puzzle solutions. The 8-puzzle is a `3x3` puzzle with 8 tiles, numbered `1-8`. The last tile is the blank tile, which can be moved around to change the state of the puzzle and move it closer to the goal. In this project, there are four possible goal states of the 8-puzzle and they are as follows:

|Goal State 1|Goal State 2|Goal State 3| Goal State 4
|--|--|--|--|
|<table><tr><td>1</td><td>2</td><td>3</td></tr><tr><td>4</td><td>5</td><td>6</td></tr><tr><td>7</td><td>8</td><td></td></tr> </table>| <table><tr><td>1</td><td>2</td><td>3</td></tr><tr><td>8</td><td></td><td>4</td></tr><tr><td>7</td><td>6</td><td>5</td></tr></table>|<table><tr><td></td><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td><td>5</td></tr><tr><td>6</td><td>7</td><td>8</td></tr></table>|<table><tr><td>1</td><td>2</td><td>3</td></tr><tr><td>4</td><td>5</td><td>6</td></tr><tr><td></td><td>7</td><td>8</td></tr></table>



This project contains four files, each serving a different function in the 8-puzzle.

`dataStructure.py:` Has one class, PriorityQueue, which orders its elements by functions. The priority queue is used to store paths which could lead to a solution.

`heuristics.py:` Contains the heuristic functions and and other helper functions.

`main.py:` Driver of program. Validates user input and sets everything up for puzzle to be solved.

`puzzle.py:` Where the puzzle is created and solved (using the A* algorithm)

---

# Run Program

To run this program, use the following command:

>python main.py <i>puzzle</i>

where <i>puzzle</i> is a 2D list with 3 rows and 3 columns and containing each number 0-8 where 0 represents the blank tile. You will then be asked to select a goal state and heuristic to aid in the search.
