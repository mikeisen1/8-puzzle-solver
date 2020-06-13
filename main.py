import puzzle
import sys
import re

#verifies inputs and solves the puzzle
def main():
    argPuzzle = sys.argv[1]
    puzzleLst = []
    #example valid initial puzzle: [[1,3,6],[7,0,5],[4,2,8]]

    #checking if command line arguments are valid
    if len(sys.argv) == 2 and validInitialState(argPuzzle):
        #converting puzzle argument to its int list representation
        puzzleLst = stringToIntLst(argPuzzle)
        #checking the puzzle contains numbers 0-8 once each
        if not validPuzzle(puzzleLst):
            sys.exit("Invalid Puzzle. The puzzle must be of format [[a,b,c],[d,e,f],[g,h,i]] where each entry is a number 0-8, and every number 0-8 appears exactly once. Use 0 to represnt the blank tile.")
    else:
        sys.exit("Invalid Arguments. Must only have 2 argyuments (main.py and puzzle) and the puzzle should be of format [[a,b,c],[d,e,f],[g,h,i]] where each entry is a digit.")

    #obtaining solvable goal state
    goal = getGoal(puzzleLst)
    #choosing the heuristic function to solve the puzzle
    heuristic = chooseHeuristic()
    #solving and printing the puzzle
    puzzle.solvePuzzle(puzzleLst,goal,heuristic)

#allows the user to choose the heuristic used to solve the puzzle.
def chooseHeuristic():
    print("What heuristic do you want to use to solve the puzzle?")
    print("A: Manhattan Distance")
    print("B: Misplaced Tiles")
    print("C: Nilsson Heuristic")
    print("D: Linear Conflicts")
    print("E: XY Heuristic")
    #want user to keep making a selection until a valid choice is made
    while True:
        #obtaining the user input
        chosen_heuristic = input("Selection: ")
        #ensures the user input is valid
        if re.search("^[a-eA-E]$",chosen_heuristic) == None:
            print("Invalid Selection. Try Again.")
        else:
            return chosen_heuristic

#allows the user to choose between 4 possible goal states of the 8-puzzle. While
    #there are many other possible goal states to the puzzle, these are the most
    #common goal states.
def getGoal(lst):
    print("What should be the goal state of the puzzle?")
    print("A: [1,2,3]\n   [4,5,6]\n   [7,8, ]")
    print("")
    print("B: [1,2,3]\n   [8, ,4]\n   [7,6,5]")
    print("")
    print("C: [ ,1,2]\n   [3,4,5]\n   [6,7,8]")
    print("")
    print("D: [1,2,3]\n   [4,5,6]\n   [ ,7,8]")
    #want user to keep making a selection until a valid choice has been made.
        #When the user makes a valid selection, the puzzle is then checked to
        #determine if it is solvable. If the puzzle is not solvable, the user
        #must choose another goal state.
    while True:
        #obtaining user input
        chosen_goal = input("Selection: ")
        if chosen_goal == "a" or chosen_goal == "A":
            #chosen goal state for puzzle
            tempGoal = [[1,2,3],[4,5,6],[7,8,0]]
            #determining if puzzle is solvable
            if isSolvable(lst,tempGoal):
                #puzzle is solvable and we have a valid goal state
                return tempGoal
            else:
                #puzzle is not solvable and the user must choose another goal
                    #state
                print("Puzzle not solvable. Choose another goal state.")
        elif chosen_goal == "b" or chosen_goal == "B":
            tempGoal = [[1,2,3],[8,0,4],[7,6,5]]
            if isSolvable(lst,tempGoal):
                return tempGoal
            else:
                print("Puzzle not solvable. Choose another goal state.")
        elif chosen_goal == "c" or chosen_goal == "C":
            tempGoal = [[0,1,2],[3,4,5],[6,7,8]]
            if isSolvable(lst,tempGoal):
                return tempGoal
            else:
                print("Puzzle not solvable. Choose another goal state.")
        elif chosen_goal == "d" or chosen_goal == "D":
            tempGoal = [[1,2,3],[4,5,6],[0,7,8]]
            if isSolvable(lst,tempGoal):
                return tempGoal
            else:
                print("Puzzle not solvable. Choose another goal state.")
        else:
            #user did not make a valid selection and must try again
            print("Invalid Selection. Try Again.")

#This function determines if the puzzle (start) is solvable given the goal
    #state (end). It does so by counting the number of inversions. An inversion
    #exists between two tiles A and B if A appears prior to B in the start state
    #(start) but B appears prior to A in the goal state (end). If the number of
    #inversions is even, the puzzle is solvable. If the number of inversions is
    #odd, the puzzle is not solvable. The blank (0) tile is not considered when
    #counting the number of inversions.
def isSolvable(start,end):
    inversions = 0
    #converting start and goal state to 1D list. This makes it easier to
        #determine the number of inversions.
    newStart = multiTo1DLst(start)
    newEnd = multiTo1DLst(end)
    for i in range(len(newStart)):
        if newStart[i] != 0:
            #determining the index, in the goal state, of the tile that appears
                #prior to the tiles that appear after it in the initial state.
            indexStart = newEnd.index(newStart[i])
            for j in range(i+1,len(newStart)):
                if newStart[j] != 0:
                    #determining the index, in the goal state, of the tile that
                        #appears after newStart[i] in the initial state.
                    indexEnd = newEnd.index(newStart[j])
                    if indexStart > indexEnd:
                        inversions += 1
    if inversions % 2 == 0:
        #number of inversions is even
        return True
    else:
        #number of inversions is odd
        return False

#converts a 2D list to a 1D list. For example, [[1,2,3],[4,5,6],[7,8,0]] will
    #become [1,2,3,4,5,6,7,8,0].
def multiTo1DLst(lst):
    oneDList = []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            oneDList.append(lst[i][j])
    return oneDList

#converts a string to a 2D list of integers. This assumes that the string given
    #will result in a valid list, as it should be used after the
    #validInitialState function.
def stringToIntLst(str):
    intLst = []
    numCount = 0
    for i in range(len(str)):
        if str[i] != '[' and str[i] != ',' and str[i] != ']':
            #if numCount is divisible by 3, we have filled a row and must add a
                #new row to the list
            if numCount % 3 == 0:
                intLst.append([])
            #placing integer into proper element of list
            intLst[int(numCount / 3)].append(int(str[i]))
            numCount += 1
    return intLst

#Checks if the initial state given is valid. It is valid if it is a 2D list with
    #3 rows and 3 columns in each row. Each entry must be a digit and the
    #entries and rows must be separated by a comma.
def validInitialState(str):
    #performs check using regular expressions
    return re.search("^\[\[\d,\d,\d\],\[\d,\d,\d\],\[\d,\d,\d\]\]$",str) != None

#determines is the puzzle (lst) chosen by the user is valid. We have already
    #checked that the size of the puzzle is valid, as that check is performed
    #by validInitialState, which is called prior to this function. Additionally,
    #the parameter lst will have been converted from a string to an int list,
    #using stringToIntLst. A puzzle is valid if every number, from 0-8, with 0
    #representing the blank tile, is in the puzzle.
def validPuzzle(lst):
    #going through numbers 0-8.
    for i in range(9):
        inLst = False
        for j in range(len(lst)):
            if i in lst[j]:
                inLst = True
                break
        if not inLst:
            return False
    return True

#calls the main() function, where the puzzle is created and solved
if __name__ == '__main__':
    main()
