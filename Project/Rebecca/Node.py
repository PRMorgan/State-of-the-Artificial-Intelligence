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
    if self.layer != 0: #no sigmoid for the inputs and bias
      self.outputValue = self.sigmoid(self.inputSum)

    for i in self.outputConnections: #for each connection
        if i.enabled: #dont do shit if not enabled
            i.toNode.inputSum += i.weight * self.outputValue #add the weighted output to the sum of the inputs of whatever node this node is connected to

#---------------------------------------
# -------------------------------------------------------------------------------------------------
#not used
  def stepFunction(self, x):
    if x < 0:
      return 0
    else:
      return 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#sigmoid activation function
  def sigmoid(self, x):
    ##OG was -4.9 * x
    if x < 0:
      return 1 / (1 + math.exp(4.9 * x))
    else:
      return 1/(1 + math.exp((-4.9) * x))
 #----------------------------------------------------------------------------------------------------------------------------------------------------------
 #returns whether this node connected to the parameter node
 #used when adding a new connection 
  def isConnectedTo(self, node):
    if node.layer == self.layer: #nodes in the same layer cannot be connected
      return False

    #you get it
    if node.layer < self.layer:
      for  i in range(len(node.outputConnections)):
        if node.outputConnections[i].toNode == self:
          return True
    else:
      for i in range(len(self.outputConnections)):
          if self.outputConnections[i].toNode == node:
              return True
    return False

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  #returns a copy of this node
  def clone(self):
    clone = Node(self.number)
    clone.layer = self.layer
    return clone
