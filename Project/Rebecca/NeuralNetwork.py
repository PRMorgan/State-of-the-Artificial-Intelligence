import math
import random


class NeuralNetwork():
    def __init__(self):
        self.nodes = []
    def createNode(self):
        self.nodes.append
    

class Node():
    def __init__(self, num):
        self.number = num
        self.edges = []
        self.inputSum = 0
        self.outputValue = 0
        
        self.layer = 0

        #of type connection gene - when we get there
        self.outputConnections = []

        #create a PVector maybe? Is this just an array of players? 
        # --> in c++: PVector drawPos = new PVector();

    def engage(self):
        """
        used to output all 
        """
        # no sigmoid for the inputs and bias
        if layer != 0:
            self.outputValue = sigmoid(inputSum);

        for connection in self.outputConnections:
            if connection.enabled == True:
                #connection will have toNode
                connection.toNode.inputSum += connection.weight * self.outputValue;
    
    # sigmoid activation function
    def sigmoid(self, x):
        y = 1 / (1 + pow((math.e, -4.9*x)))
        return y

    #   //returns whether this node connected to the parameter node
    #   //used when adding a new connection 
    def isConnectedTo(self, node):
        if node.layer == self.layer:
            return False
        
        if node.layer < self.layer:
            for node_iteration in node.outputConnections:
                if node_iteration.toNode == self:
                    return True
        else:
            for node_iteration in self.outputConnections:
                if node_iteration.toNode == node:
                    return True

    def cloneNode(self):
        clone = Node(self.number)
        clone.layer = layer
        return clone


class connectionGene():
    def __init__(self, source, destination, weight, innovation):
        #node
        self.fromNode = source
        #node
        self.toNode = destination
        #float
        self.weight = weight
        #int
        self.innovation = innovation
        enabled = True
    def mutateWeight(self):
        rand2 = random.randint(100)
        if rand2 < 10:
            self.weight = random.uniform(-1,1)
        else: 
            self.weight += random.normalvariate(0, 1)/50
            if self.weight > 1: self.weight = 1
            if self.weight < -1: self.weight = -1
    
    def clone(self, source, destination):
        clone = connectionGene(source, destination, self.weight, self.innovation)
        clone.enabled = self.enabled
        return clone

class connectionHistory():
    def __init__(self, source, destination, inno, innovationNos):
        self.fromNode = source
        self.toNode = destination
        self.innovationNumber = inno

        # Might cause an issue
        self.innovationNumbers = innovationNos.clone()

    def matches(self, genome, source, destination):
        if genome.genes.size() == self.innovationNumber.size():
            if source.number == self.fromNode and destination.number == self.toNode:
                for gene in genome:
                    if gene.innovationNumber not in self.innovationNumbers:
                        return False
                return True
        else:
            return False
