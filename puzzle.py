import copy
import dataStructure
import heuristics
import os
import time

class Puzzle:
    #initializes the Puzzle
    def __init__(self, puzzle, goal):
        self.puzzle = puzzle
        self.goal = goal

    #checks if the argument goal is a goal state of the puzzle
    def isGoalState(self, goal):
        for i in range(len(self.goal)):
            if goal[i] != self.goal[i]:
                return False
        return True

    #finds position of blank tile, which is represented by the integer 0
    def position(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                #checking if the current element being evaluated is 0
                if 0 == state[i][j]:
                    return (i, j)
        #returned if there is no zero in the current state. However, this should
            #never happen if a puzzle is created properly.
        return (-1,-1)

    #general A* search
    def aStarSearch(self, queue, val):
        usedStates = []

        queue.push([(self.puzzle, 0)])
        #general case, where we want to find the full solution to the puzzle
        if val == 0:
            #counts the total number of states visited in the search
            nodesExpanded = 0
            while not queue.isEmpty():
                #path: list of tuples - (8-puzzle state, cost to 8-puzzle state)
                path = queue.pop() #path with shortest f(x)+h(x)

                #checking if we have reached the goal state.
                if self.isGoalState(path[-1][0]): #path[-1][0] is the state we need to look at
                    return (path, nodesExpanded)

                #if the current state has not been visited, then we need to
                    #visit that state. We then check, for each direction, if the
                    #blank tile can be moved in that direction. If so, we create
                    #a new path containing the current path we popped from the
                    #queue and the new state when the blank tile is moved in a
                    #new direction. We then add the cost of that new path (cost
                    #to current path + 1) to create a tuple and add that tuple
                    #to the queue. Note that the blank tile can only move one
                    #tile at a time either horizontally or vertically along the
                    #puzzle.

                #NOTE: path[-1][1] is the cost to the last state in the path.
                if path[-1][0] not in usedStates:
                    #adding the current state being visited to the tracking list
                        #usedStates
                    usedStates.append(path[-1][0])
                    #we are now expanding a node
                    nodesExpanded += 1
                    #need this to determine successors of current state
                    (row, col) = self.position(path[-1][0])

                    if row != 0:
                        #can swap the blank tile with the tile in the same
                            #column but one row above
                        successorPath = copyPath(path)
                        currentState = copyLst(successorPath[-1][0])
                        successorState = swap(currentState, row, col, row - 1, col)
                        successorPath.append((successorState, path[-1][1] + 1))
                        queue.push(successorPath)

                    if row != 2:
                        #can swap the blank tile with the tile in the same
                            #column but one row below
                        successorPath = copyPath(path)
                        currentState = copyLst(successorPath[-1][0])
                        successorState = swap(currentState, row, col, row + 1, col)
                        successorPath.append((successorState, path[-1][1] + 1))
                        queue.push(successorPath)

                    if col != 0:
                        #can swap the blank tile with the tile in the same
                            #row but one column to the left
                        successorPath = copyPath(path)
                        currentState = copyLst(successorPath[-1][0])
                        successorState = swap(currentState, row, col, row, col - 1)
                        successorPath.append((successorState, path[-1][1] + 1))
                        queue.push(successorPath)

                    if col != 2:
                        #can swap the blank tile with the tile in the same
                            #row but one column to the right
                        successorPath = copyPath(path)
                        currentState = copyLst(successorPath[-1][0])
                        successorState = swap(currentState, row, col, row, col + 1)
                        successorPath.append((successorState, path[-1][1] + 1))
                        queue.push(successorPath)

            #returned in the situation that no solution is found. However, the
                #puzzle should have a solution for its goal state, or this
                #search will take a long time to find the solution. The
                #existence of the solution should be verified prior to
                #performing the search, as we simply need to count the number
                #of inversions.
            return (([[0,0,0],[0,0,0],[0,0,0]],-1), -1)
        #used when we do the A* with XY heuristic search. This is for the row
            #search portion of calculating the heuristic value. The biggest
            #difference with the general A* search is only vertical moves are
            #valid moves and the ordering of the tiles in the rows does not
            #matter (we just want the tiles to be in their correct goal row).
        elif val == 1:
            while not queue.isEmpty():
                path = queue.pop()
                #checking if each tile is in its correct goal state row.
                if heuristics.isXYGoalStateRow(path[-1][0], self.goal):
                    return (path[-1][0],path[-1][1])

                #checking if the current state has already been visited
                if path[-1][0] not in usedStates:
                    (row, column) = self.position(path[-1][0])
                    if row == 0:
                        def rowZeroEval():
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,row+1,i)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        rowZeroEval()
                    elif row == 1:
                        def rowOneEval(delta):
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,row+delta,i)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        rowOneEval(1)
                        rowOneEval(-1)
                    elif row == 2:
                        def rowTwoEval():
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,row-1,i)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        rowTwoEval()
            #returned if there is no solution where each tile is in its proper
                #goal state row.
            return ([[0,0,0],[0,0,0],[0,0,0]], -1, -1)
        else:
            #This is similar to where val == 1, except here only horizontal
                #(column) moves are valid.
            while not queue.isEmpty():
                path = queue.pop()

                if heuristics.isXYGoalStateColumn(path[-1][0],self.goal):
                    return (path[-1][0],path[-1][1])

                if path[-1][0] not in usedStates:
                    (row, column) = self.position(path[-1][0])
                    if column == 0:
                        def columnZeroEval():
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,i,column+1)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        columnZeroEval()
                    elif column == 1:
                        def columnOneEval(delta):
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,i,column+delta)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        columnOneEval(1)
                        columnOneEval(-1)
                    elif column == 2:
                        def columnTwoEval():
                            for i in range(3):
                                newPath = copyPath(path)
                                tempNewState = copyLst(newPath[-1][0])
                                newCost = path[-1][1] + 1
                                newState = swap(tempNewState,row,column,i,column-1)
                                newPath.append((newState,newCost))
                                queue.push(newPath)
                        columnTwoEval()
            #returned if there is no solution where each tile is in its proper
                #goal state column.
            return ([[0,0,0],[0,0,0],[0,0,0]], -1, -1)

    #For the heuristic functions, we will know and apply the arguments later.
        #Thus, we use lambdas (anonymous functions). Also, len(x) is the current
        #cost of the path.

    #creating the heuristic and queue for A* with Manhattan Distance heuristic
        #search.
    def aStarManhattanHeuristic(self,val):
        if val == 0:
            f = lambda x: len(x) + heuristics.manhattanCost(x[-1][0], self.goal)
            h = lambda x: heuristics.manhattanCost(x[-1][0], self.goal)
            queue = dataStructure.PriorityQueue((f,h))
            return self.aStarSearch(queue,val)
        elif val == 1:
            #used in computation of XY heuristic.
            f = lambda x: len(x) + heuristics.rowManhattan(x[-1][0],self.goal)
            h = lambda x: heuristics.rowManhattan(x[-1][0], self.goal)
            queue = dataStructure.PriorityQueue((f,h))
            return self.aStarSearch(queue,val)
        else:
            #used in computation of XY heuristic.
            f = lambda x: len(x) + heuristics.colManhattan(x[-1][0],self.goal)
            h = lambda x: heuristics.colManhattan(x[-1][0],self.goal)
            queue = dataStructure.PriorityQueue((f,h))
            return self.aStarSearch(queue,val)

    #creating the heuristic and queue for A* with Misplaced Tiles heuristic
        #search.
    def aStarMisplacedTiles(self):
        f = lambda x: len(x) + heuristics.misplacedTiles(x[-1][0], self.goal)
        h = lambda x: heuristics.misplacedTiles(x[-1][0], self.goal)
        queue = dataStructure.PriorityQueue((f,h))
        return self.aStarSearch(queue,0)

    #creating the heuristic and queue for A* with Nilsson Heuristic search.
    def aStarNilssonHeuristic(self):
        f = lambda x: len(x) + heuristics.nilssonSequenceScore(x[-1][0],self.goal)
        h = lambda x: heuristics.nilssonSequenceScore(x[-1][0],self.goal)
        queue = dataStructure.PriorityQueue((f,h))
        return self.aStarSearch(queue,0)

    #creating the heuristic and queue for A* with Linear Conflicts heuristic
        #search.
    def aStarLinearConflicts(self):
        f = lambda x: len(x) + heuristics.linearConflicts(x[-1][0], self.goal)
        h = lambda x: heuristics.linearConflicts(x[-1][0], self.goal)
        queue = dataStructure.PriorityQueue((f,h))
        return self.aStarSearch(queue,0)

    #creating the heuristic and queue for A* with XY Heuristic search.
    def aStarXYHeuristic(self):
        f = lambda x: len(x) + heuristics.xyCostHeuristic(x[-1][0],self.goal)
        h = lambda x: heuristics.xyCostHeuristic(x[-1][0],self.goal)
        queue = dataStructure.PriorityQueue((f,h))
        return self.aStarSearch(queue,0)

#solves the puzzle from the start state (start) to the chosen goal state (goal)
    #using the chosen heuristic (heuristic). The parameter heuristic will be a
    #one character string, and there is a series of if-else statements, which
    #evaluate the heuristic parameter value, to determine how the puzzle is
    #solved. After solving the puzzle, this function prints out the states, one
    #step at a time, from the start state to the goal state. There is a one
    #second break in between the print statements so each state can be fully
    #understood and followed.
def solvePuzzle(start,goal,heuristic):
    #creating the puzzle
    puzzleToSolve = Puzzle(start,goal)
    (path,nodesExpanded) = ([],0)
    if heuristic == "a" or heuristic == "A":
        (path,nodesExpanded) = puzzleToSolve.aStarManhattanHeuristic(0)
    if heuristic == "b" or heuristic == "B":
        (path,nodesExpanded) = puzzleToSolve.aStarMisplacedTiles()
    if heuristic == "c" or heuristic == "C":
        (path,nodesExpanded) = puzzleToSolve.aStarNilssonHeuristic()
    if heuristic == "d" or heuristic == "D":
        (path,nodesExpanded) = puzzleToSolve.aStarLinearConflicts()
    if heuristic == "e" or heuristic == "E":
        (path,nodesExpanded) = puzzleToSolve.aStarXYHeuristic()
    os.system('clear')
    #prints path from initial state to goal state
    for (state, cost) in path:
        for i in range(len(state)):
            print("+-+-+-+")
            print("|",end="")
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    print(" ",end="|")
                else:
                    print(state[i][j],end="|")
            print("")
        print("+-+-+-+")
        #displays the cost to the current state
        print("Moves:",cost)
        time.sleep(1)
        #clears the screen so the next state is printed "on top of" the
            #previous state
        os.system('clear')
    os.system('clear')

#creates a deep copy of a 2D list
def copyLst(lst):
    newLst = []
    for i in range(len(lst)):
        newLst.append([])
        for j in range(len(lst[i])):
            newLst[i].append(lst[i][j])
    return newLst

#creates a deep copy of a list of tuples. This is for creating a copy of a
    #puzzle path
def copyPath(path):
    newPath = []
    for element in path:
        (state, cost) = element
        newStateList = []
        for i in range(3):
            newStateList.append([])
            for j in range(3):
                newStateList[i].append(state[i][j])
        newPath.append((newStateList, cost))
    return newPath

#swaps the positions for elements r1,c1 and r2,c2 of a 2D list
def swap(lst, r1, c1, r2, c2):
    temp = lst[r1][c1]
    lst[r1][c1] = lst[r2][c2]
    lst[r2][c2] = temp
    return lst
