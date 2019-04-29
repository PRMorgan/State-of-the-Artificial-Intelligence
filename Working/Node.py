import math

class Node():
    #constructor
  def __init__(self, no):
    self.pos = (0,0)
    self.title = None
    self.number = no
    self.inputSum = 0 #current sum i.e. before activation
    self.outputValue = 0.0 #after activation function is applied
    self.outputConnections = []
    self.layer = 0
    self.pos = (0,0)

  #the node sends its output to the inputs of the nodes its connected to
  def engage(self):
    if self.layer != 0: #no sigmoid for the inputs and bias
      self.outputValue = self.sigmoid(self.inputSum)

    for i in self.outputConnections: #for each connection
        if i.enabled: #dont do anything if not enabled
            i.toNode.inputSum += i.weight * self.outputValue #add the weighted output to the sum of the inputs of whatever node this node is connected to

#sigmoid activation function
  def sigmoid(self, x):
    y = 1 / (1 + pow(math.e, -4.9*x))
    return y

 #returns whether this node connected to the parameter node
 #used when adding a new connection 
  def isConnectedTo(self, node):
    if node.layer == self.layer: #nodes in the same layer cannot be connected
      return False

    if node.layer < self.layer:
      for  i in range(len(node.outputConnections)):
        if node.outputConnections[i].toNode == self:
          return True
    else:
      for i in range(len(self.outputConnections)):
          if self.outputConnections[i].toNode == node:
              return True
    return False

  #returns a copy of this node
  def clone(self):
    clone = Node(self.number)
    clone.layer = self.layer
    clone.pos = self.pos
    clone.title = self.title
    return clone
