import puzzle
import dataStructure

#---------------------------------------------------------#
#-------------------Manhattan Heuristic-------------------#

#The Manhattan heuristic value is the sum of each tile's horizontal and
    #vertical distance to its goal position. For example, if the tile '4' is in
    #position [2,2] in the current state and its goal position is [1,0], then
    #its Manhattan distance to its goal position is (2-1) + (2-0) = 3. Note that
    #in the following functions, abs() is used. That ensures that if a tile's
    #current row or column position is lower value than its goal row or column
    #position, we are not computing a negative Manhattan distance for that tile.

#Computes the column Manhattan distance of tiles, ignoring their row positions
    #in the goal state. This is used in the computation of the XY heuristic
def colManhattan(lst,goal):
    sum = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != 0:
                (_, goalY) = indexMultiList(goal, lst[i][j])
                sum += abs(j - goalY)

    return sum

#Computes the row Manhattan distance of tiles, ignoring their column positions
    #in the goal state. This is used in the computation of the XY heuristic
def rowManhattan(lst, goal):
    sum = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != 0:
                (goalX, _) = indexMultiList(goal, lst[i][j])
                sum += abs(i - goalX)

    return sum

#Computes the sum of the Manhattan distances of the tiles to their goal
    #postions.
def manhattanCost(lst, goal):
    sum = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            #we do not compute the Manhattan distance for the blank (0) tile
            if lst[i][j] != 0:
                #must know goal position to compute manhattan distance for tile
                (goalX, goalY) = indexMultiList(goal, lst[i][j])
                sum += (abs(i - goalX) + abs(j - goalY))

    return sum

#-----------------End Manhattan Heuristic-----------------#
#---------------------------------------------------------#



#---------------------------------------------------------#
#----------------Misplaced Tiles heuristic----------------#

#The misplaced tiles heuristic simply computes the number of tiles that are
    #misplaced, or not in their goal position. The blank (0) tile is ignored.

def misplacedTiles(lst, goal):
    count = 0
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] != goal[i][j] and lst[i][j] != 0:
                count += 1
    return count

#----------------Misplaced Tiles Heuristic----------------#
#---------------------------------------------------------#



#---------------------------------------------------------#
#--------------------Nilsson Heuristic--------------------#

#The Nilsson Heuristic relies on two parts, the Nilsson Sequence Score and the
    #total Manhattan cost. The Nilsson sequence score can be expressed as
    #score = 3*C(lst) = 3(2*clockwise(lst) + center(lst)). For clockwise(lst),
    #for each tile in the puzzle, if the tile clockwise to it is not the tile
    #that should be clockwise to it, add one. It does not consider the center
    #tile. For center(lst), if there is a tile in the center, add 1. The
    #sequence score ingores the blank (0) tile in the computation of the score.
    #We then add the sequence score to the total Manhattan Cost of the tiles to
    #their goal positions.

def nilssonSequenceScore(lst,goal):
    score = 0

    #convert to Nilsson 1D list to make computation of sequence score easier and less complex
    lstSingle = puzzleStateto1DList(lst)

    for i in range(0,7):
        if lstSingle[i] != 0 and (lstSingle[i]) + 1 != (lstSingle[i+1]):
            score += 2
    if lstSingle[7] != 0 and (lstSingle[7]) + 1 != (lstSingle[0]):
        score += 2
    if lstSingle[8] != 0:
        score += 1

    score *= 3
    return score + manhattanCost(lst,goal)

#------------------End Nilsson Heuristic------------------#
#---------------------------------------------------------#



#---------------------------------------------------------#
#---------------Linear Conflicts Heuristic----------------#

#The Linear Conflicts Heuristic relies on two parts, computing the number of
    #linear conflicts and the Manhattan Cost. To count the number of linear
    #conflicts, we go row by row and then column by column. For each row (or
    #column), a linear conflict between two tiles exist if the two tiles are in
    #their goal row (or column) and one of the tiles would have to move out of
    #the way for the other tile to reach its goal position. We sum the number
    #of linear conflicts and then multiply that value by two. We then sum that
    #value (linear conflicts * 2) and the total Manhattan cost of the tiles in
    #the current state.

def linearConflicts(lst,goal):
    numberConflicts = 0

    for i in range(len(lst)):
        rowConflicts = [0,0,0]
        for j in range(len(lst[i]) - 1):
            if lst[i][j] != 0:
                for k in range(j+1,len(lst[i])):
                    (currentgoalrow, currentgoalcol) = indexMultiList(goal, lst[i][j])
                    (othergoalrow, othergoalcol) = indexMultiList(goal,lst[i][k])
                    if lst[i][k] != 0 and currentgoalrow == othergoalrow and currentgoalcol > othergoalcol and currentgoalrow == i:
                        rowConflicts[j] += 1
                        rowConflicts[k] += 1
            else:
                rowConflicts[j] = 10 #take minimum rowConflicts value, but never want to choose
                                     #where value of tile is 0, as it always has 0 conflicts
        tempMin = 0
        for num in rowConflicts:
            if num != 0 and num != 10:
                if tempMin == 0:
                    tempMin = num
                elif tempMin > num:
                    tempMin = num
        numberConflicts += tempMin

    for col in range(len(lst[0])):
        colConflicts = [0,0,0]
        for row in range(len(lst) - 1):
            if lst[row][col] != 0:
                for k in range(row+1,len(lst)):
                    (currentgoalrow, currentgoalcol) = indexMultiList(goal, lst[row][col])
                    (othergoalrow, othergoalcol) = indexMultiList(goal,lst[k][col])
                    if currentgoalcol == othergoalcol and currentgoalrow > othergoalrow and currentgoalcol == col:
                        colConflicts[row] += 1
                        colConflicts[k] += 1
            else:
                colConflicts[col] = 10 #take minimum rowConflicts value, but never want to choose
                                     #where value of tile is 0, as it always has 0 conflicts
        tempMin = 0
        for num in colConflicts:
            if num != 0 and num != 10:
                if tempMin == 0:
                    tempMin = num
                elif tempMin > num:
                    tempMin = num
        numberConflicts += tempMin

    return numberConflicts*2 + manhattanCost(lst, goal)

#-------------End Linear Conflicts Heuristic--------------#
#---------------------------------------------------------#



#---------------------------------------------------------#
#----------------------XY Heuristic-----------------------#

#In the XY heuristic, we are calculating the sum of the minimum number of column
    #moves such that each tile is in its correct goal column and the minimum
    #number of row moves such that each tile is in its correct goal row. The
    #column move and row move computations are done separately. A move is only
    #valid, for this heuristic, if one of the tiles being moved (or swapped) is
    #the blank (0) tile.

#Checking, for the row moves part of the heuristic, if every tile is in its
    #correct row.
def isXYGoalStateRow(lst, goal):
    for i in range(3):
        for j in range(3):
            #checking if the list element is in its correct row
            if lst[i][j] not in goal[i]:
                return False
    return True

#Checking, for the column moves part of the heuristic, if every tile is in its
    #correct column
def isXYGoalStateColumn(lst,goal):
    for i in range(3):
        for j in range(3):
            #need to find the location of the tile in the goal state to
            #determine if the goal column matches the current column position
            #of the element of the list (lst)
            (_,goalc) = indexMultiList(goal,lst[i][j])
            if j != goalc:
                return False
    return True

#The following function computes the heuristic value. An A* search with a
    #Manhattan heuristic is used to find the minimum number of row and column
    #moves for each element to be in its goal row or column. We get the minimum
    #number of moves by obtaining the path length (cost) returned by the A*
    #searches.
def xyCostHeuristic(lst,goal):
    p = puzzle.Puzzle(lst,goal)

    #Row moves aspect of the heurstic. rowMoves is the minimum number of row
    #moves required for each element to be in its goal row.
    (_,rowMoves) = p.aStarManhattanHeuristic(1)

    #Column moves aspect of the heurstic. columnMoves is the minimum number of
    #column moves required for each element to be in its goal column.
    (_,columnMoves) = p.aStarManhattanHeuristic(2)
    return rowMoves + columnMoves
#---------------------End XY Heuristic--------------------#
#---------------------------------------------------------#

#This returns the position of a given element in a 2-dimensional list. It is
    #used in the computation of the Manhattan Cost, Linear Conflicts, and XY
    #Cost heuristics. This function is also used in the Linear Conflicts
    #heuristics, as that relies partially on the Manhattan Cost.
def indexMultiList(lst, element):
    for i in range(len(lst)):
        if element in lst[i]:
            return (i, lst[i].index(element))

    return (-1, -1)

#This function converts a 2-dimensional list into a 1-dimensional list. It is
    #intended for use in the computation of the Nilsson Heuristic.
def puzzleStateto1DList(lst):
    newList = []
    newList.append(lst[0][0])
    newList.append(lst[0][1])
    newList.append(lst[0][2])
    newList.append(lst[1][2])
    newList.append(lst[2][2])
    newList.append(lst[2][1])
    newList.append(lst[2][0])
    newList.append(lst[1][0])
    newList.append(lst[1][1])
    return newList
