import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
"""
What we are doing is creating a set of base nodes and then we will sub divide
the arcs from  to form a more complex fake network that roughly mimics a real network.
Each of these base nodes represent a change over between routes, and is connected to atleast 3 other base nodes.
"""
NumberOfBaseNodes = 7
np.random.seed(5)
BaseMatrix = np.zeros((NumberOfBaseNodes,NumberOfBaseNodes) , dtype=int)
ConectionVector = np.random.randint(0,10,(NumberOfBaseNodes))
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

RandomNumberMatrix = np.random.randint(3,5 , size = (NumberOfBaseNodes, NumberOfBaseNodes))
CondencedMatrix = RandomNumberMatrix * BaseMatrix #this is a matrix that represents the number of nodes between any of the big nodes.
TotalNumberOfNodes = np.sum(CondencedMatrix) - np.sum(BaseMatrix) + NumberOfBaseNodes

print(CondencedMatrix)
print(TotalNumberOfNodes)

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

AdjacentDuelMatrix = np.zeros((Indexer,Indexer) , dtype = int)

for y , Row in enumerate(BigMatrix):
    for x , Point in enumerate(Row):
        if Point != 0:
            for Arc in BigMatrix[x]:
                if Arc != 0:
                    AdjacentDuelMatrix[Point][Arc] = 1



a = nx.convert_matrix.from_numpy_matrix(BaseMatrix)
nx.draw_networkx(a)
plt.show()

a = nx.convert_matrix.from_numpy_matrix(BigMatrix)
nx.draw_networkx(a)
plt.show()

print(CondencedMatrix)
print(" ")
print(BigMatrix)
print(" ")
print(AdjacentDuelMatrix)

Important 



#Now for calculating the duel of that matrix
#For each node 