import math

class Node():
  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  #constructor
  def __init__(self, no):
    self.number = no
    self.inputSum = 0 #current sum i.e. before activation
    self.outputValue = 0.0 #after activation function is applied
    self.outputConnections = []
    self.layer = 0

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  #the node sends its output to the inputs of the nodes its connected to
  def engage(self):
    if layer != 0: #no sigmoid for the inputs and bias
      outputValue = sigmoid(inputSum)

    for i in range(len(outputConnections)): #for each connection
        if outputConnections[i].enabled: #dont do shit if not enabled
            outputConnections[i].toNode.inputSum += outputConnections[i].weight * outputValue #add the weighted output to the sum of the inputs of whatever node this node is connected to

#----------------------------------------------------------------------------------------------------------------------------------------
#not used
  def stepFunction(x):
    if x < 0:
      return 0
    else:
      return 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#sigmoid activation function
  def sigmoid(x):
    y = 1 / (1 + pow(math.e, -4.9*x))
    return y
 #----------------------------------------------------------------------------------------------------------------------------------------------------------
 #returns whether this node connected to the parameter node
 #used when adding a new connection 
  def isConnectedTo(node):
    if node.layer == layer: #nodes in the same layer cannot be connected
      return False

    #you get it
    if node.layer < layer:
      for  i in range(len(node.outputConnections)):
        if node.outputConnections[i].toNode == self:
          return True
    else:
      for i in range(len(self.outputConnections)):
          if self.outputConnections[i].toNode == self.node:
              return True
    return False;

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  #returns a copy of this node
  def clone():
    clone = Node(self.number)
    clone.layer = self.layer
    return clone
