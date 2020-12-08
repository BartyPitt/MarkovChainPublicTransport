import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

def RandomMatrixGenerator(seed , BaseNodes):
    """
    What we are doing is creating a set of base nodes and then we will sub divide
    the arcs from  to form a more complex fake network that roughly mimics a real network.
    Each of these base nodes represent a change over between routes, and is connected to atleast 3 other base nodes.
    """
    NumberOfBaseNodes = BaseNodes
    np.random.seed(seed)
    random.seed(seed)
    BaseMatrix = np.zeros((NumberOfBaseNodes,NumberOfBaseNodes) , dtype=int)
    ConectionVector = np.random.randint(2,4,(NumberOfBaseNodes))
    print(ConectionVector)

    """
    Each node selects one node from the nodes not selected and one random node 
    Except for the last that selects the first node that was selected,
    this is to stop there from being an isolated system.
    Some nodes will select multiple nodes based apon the connection vector. 
    """
    RemainingNodes = set([i for i in range(NumberOfBaseNodes)])
    PreviousNode = 0
    for i , n in enumerate(ConectionVector):
        print(PreviousNode)
        
        if i == NumberOfBaseNodes - 1: # this is to make sure that the graph is fully connected
            BaseMatrix[PreviousNode,0] = 1
            continue

        SetNotContainingNode = set([j for j in range(1,PreviousNode)] + [j for j in range(PreviousNode+1,NumberOfBaseNodes)])
        PickableNodes = RemainingNodes & SetNotContainingNode #do this better you know its one function , atleast try and find it before just commenting it and ignoring it 
        KeyNode = random.choice(list(PickableNodes)) # selects a node thats not itself.
        KeyNodes = [KeyNode]
        if n > 1:
            KeyNodes.append(random.choice(list(SetNotContainingNode)))
        for Node in KeyNodes:
            BaseMatrix[PreviousNode,Node] = 1

        PreviousNode = KeyNode
        RemainingNodes.remove(KeyNode)

    RandomNumberMatrix = np.random.randint(1,5 , size = (NumberOfBaseNodes, NumberOfBaseNodes))
    CondencedMatrix = RandomNumberMatrix * BaseMatrix #this is a matrix that represents the number of nodes between any of the big nodes.
    TotalNumberOfNodes = np.sum(CondencedMatrix) - np.sum(BaseMatrix) + NumberOfBaseNodes

    #print(CondencedMatrix)
    #print(TotalNumberOfNodes)

    BigMatrix = np.zeros((TotalNumberOfNodes, TotalNumberOfNodes) , dtype = int)
    CurrentRow = NumberOfBaseNodes
    Indexer = 1
    for j,Row in enumerate(CondencedMatrix):
        for  i , Point in enumerate(Row):

            # If the nodes are not connected , pass
            if Point == 0:
                continue
            elif Point == 1:
                BigMatrix[j][i] = Indexer
                Indexer += 1 
                continue

            else: #If the nodes are not neighbors connect to the neighbor node
                BigMatrix[j][CurrentRow] = Indexer
                Indexer += 1         

            #If there is a chain to be formed
            while Point > 1:
                if Point == 2:
                    BigMatrix[CurrentRow][i] = Indexer
                    Point = 0
                else:
                    BigMatrix[CurrentRow][CurrentRow + 1] = Indexer
                    Point -= 1
                CurrentRow += 1
                Indexer += 1

    DisplayMatrix(BigMatrix)
    BigMatrix = np.column_stack((BigMatrix , [1 for i in range(BigMatrix.shape[0])]))
    BigMatrix = np.vstack((BigMatrix , [1 for i in range(BigMatrix.shape[1])]))

    WaitingMatrix = np.random.rand(*BigMatrix.shape) * BigMatrix
    WaitingMatrix = MakeRowstochastic(WaitingMatrix)
    for i in range(len(WaitingMatrix)):
        WaitingMatrix[i][i] = WaitingTimeDistributionFunction()

    WaitingMatrix[-1][-1] = 2
    WaitingMatrix = MakeRowstochastic(WaitingMatrix)
    return WaitingMatrix



def CreateDuelMatrix(NumberedArcMatrix, NumberOfArcs):
    AdjacentDuelMatrix = np.zeros((NumberOfArcs,NumberOfArcs) , dtype = int)

    for y , Row in enumerate(NumberedArcMatrix):
        for x , Point in enumerate(Row):
            if Point != 0:
                for Arc in BigMatrix[x]:
                    if Arc != 0:
                        AdjacentDuelMatrix[Point][Arc] = 1

def DisplayMatrix(MatrixToBeDisplayed):
    a = nx.convert_matrix.from_numpy_matrix(MatrixToBeDisplayed , create_using=nx.MultiDiGraph)
    nx.draw_networkx(a)
    plt.show()
    return True



"""
Lets think about what to do next.
What we want is a set of matrices that contain all of the fun pieces of infomation.
Plan. Multiply the matrix by a random number matrix , then row stocasitc normalise.
"""


def MakeRowstochastic(InputMatrix):
    """
    Takes in a matix and makes it row stochastic
    Matrix must be a numpy matrix.
    TODO figure out if this function is functionally pure
    """
    AverageVector = np.sum(InputMatrix , axis = 1) # Find the row average
    Output = InputMatrix  / AverageVector[: , None]  #divide each of the rows by the row average.
    return Output



def WaitingTimeDistributionFunction(input = None):
    """
    Function for generating the numbers for the waiting times
    Takes a nymber returns 1-x/x of that number
    If no number is generated then it picks a number between 10 - 30
    """
    if input == None:
        input = random.randrange(start = 2 , stop = 20)
    return (input - 1) / input




#print(WaitingMatrix)



if __name__ == "__main__": 
    print("start")
    WaitingMatrix = RandomMatrixGenerator(5 , 5)
    w , v = np.linalg.eig(np.transpose(WaitingMatrix))
    #print(w) 
    print("ping")
    #print(v)

    AddInfititum = np.linalg.matrix_power(WaitingMatrix , 60)
    print("large numbers")
    print(AddInfititum)
    a = np.zeros((len(WaitingMatrix)))
    a.fill(1)
    print("A is ")
    print(a)
    b = np.matmul(a,AddInfititum)
    print(b)

    for i , Point in enumerate(w):
        #yo we got the https://0.30000000000000004.com/ joke. so this is a crude way of kinda dealing with that
        if not np.iscomplex(Point) :
            print(v[:,i])
            plt.plot(v[:,i] , "ro")
            plt.title(Point)
            plt.show()
            pass




#Now for calculating the duel of that matrix
#For each node 
