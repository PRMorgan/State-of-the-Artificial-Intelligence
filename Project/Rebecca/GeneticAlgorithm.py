import math
from NeuralNetwork import *

class Genome():
    def __init___(self, inputs, outputs):

        #contains connectionGene
        self.genes = []
        #contains Node
        self.nodes = []

        #(int)quantity of both
        self.inputs = inputs
        self.outputs = outputs
        
        #(int)
        self.layers = 2
        self.nextNode = 0

        #contains Nodes
        self.network = []

        #Create input nodes
        #might be wrong
        for i in range(len(self.inputs)):
            self.nodes.append(Node(i))
            self.nextNode += 1
            self.nodes[i].layer = 0
        
        #Create output nodes
        for i in range(len(outputs)):
            self.nodes.append(Node(i + self.inputs))
            self.nodes[i].layer = 1
            self.nextNode += 1;

        #initialize the bias node once established
        self.nodes.append(Node(self.nextNode))
        self.biasNode = self.nextNode
        self.nextNode += 1
        self.nodes[self.biasNode].layer = 0
    
    def getNode(self, nodeNumber):
        for node in self.nodes:
            if node.number == nodeNumber:
                return node
        return null
    
    def connectNodes(self):
        """adds the conenctions going out of a node to that node so that it can acess the next node during feeding forward """
        #clear all of the nodes
        for node in self.nodes:
            #unsure if clear will work
            node.outputConnections.clear()
        
        for gene in self.genes:
            gene.fromNode.outputConnections.append(gene)
    
    def feedForward(self, inputValues):
        """feeding in input values into the NN and returning output array"""
        for i in range(self.inputs):
            self.nodes[i].outputValue = inputValues[i]
        self.nodes[self.biasNode].outputValue = 1

        for node in self.network:
            node.engage()
        
        outs = []
       # for output in self.outputs:
            #make sure (int)output is giving the correct sequential output
            #outs[output] = (float)self.nodes[self.inputs + output].outputValue #<- This line is wronk
            
        for node in self.nodes:
            node.inputSum = 0
        return outs
    
    def generateNetwork(self):
        """  sets up the NN as a list of nodes in order to be engaged """
        self.connectNodes()
        network = []
        for lay in self.layers:
            for node in self.nodes:
                if node.layer == lay:
                    network.append(node)

    def addNode(self, innovationHistory):
        if self.genes.size() == 0:
            addConnection(innovationHistory)
            return
        randomConnection = math.floor(random(len(self.genes)))

        while self.genes.get(randomConnection).fromNode == nodes.get(biasNode) and self.genes.size() > 1:
            randomConnection = math.floor(random(len(self.genes)))

        self.genes.get(randomConnection).enabled = false

        newNodeNo = nextNode
        nodes.add(newNodeNo)
        nextNode = nextNode + 1

        connectionInnovationNumber = getInnovationNumber(innovationHistory, self.genes.get(randomConnection).fromNode, getNode(newNodeNo))
        #add a new connection from the new node with a weight the same as the disabled connection
        self.genes.add(connectionGene(getNode(newNodeNo), self.genes.get(randomConnection).toNode, genes.get(randomConnection).weight, connectionInnovationNumber))
        getNode(newNodeNo).layer = self.genes.get(randomConnection).fromNode.layer + 1

        connectionInnovationNumber = getInnovationNumber(innovationHistory, nodes.get(biasNode), getNode(newNodeNo))
        #Connect the bias to the new node with a weight of 0
        self.genes.add(connectionGene(self.nodes.get(biasNode), getNode(newNodeNo), 0, connectionInnovationNumber))

        #If the layer of the new node is equal to the layer of the output node of the old connection then a new layer needs to be created
        #more accurately the layer numbers of all layers equal to or greater than this new node need to be incrimented
        if (getNode(newNodeNo).layer == self.genes.get(randomConnection).toNode.layer):
              for i in self.nodes: #dont include this newest node
                  if (i.layer >= getNode(newNodeNo).layer):
                      i.layer = i.layer + 1;
              layers = layers + 1;
        connectNodes();
