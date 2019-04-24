from Node import *
from Gene import *
from History import *

import random

class NeuralNet:
    def __init__(self, inputs, outputs):
        #set input number and output number
        self.inputs = inputs
        self.outputs = outputs
        self.layers = 2
        self.nextNode = 0
        self.biasNode = 0
        self.nodes = [] #list of nodes
        self.genes = [] #list of connections between nodes which represent the NN
        self.network = [] #list of the nodes in the order that they need to be considered in the NN
        
        self.nextConnectionNo = 0

        #create input nodes
        for i in range(self.inputs):
            self.nodes.append(Node(i))
            self.nextNode += 1
            self.nodes[i].layer = 0
        
        #create output nodes
        for i in range(self.outputs):
            self.nodes.append(Node(i + self.inputs))
            self.nodes[i + self.inputs].layer = 1
            self.nextNode += 1
        self.nodes.append(Node(self.nextNode)) #bias node
        self.biasNode = self.nextNode
        self.nextNode += 1
        self.nodes[self.biasNode].layer = 0

    #returns the node with a matching number
    #sometimes the nodes will not be in order
    def getNode(self,nodeNumber):
        for i in self.nodes:
            if i.number == nodeNumber:
                return i
        return None

    #adds the conenctions going out of a node to that node so that it can acess the next node during feeding forward
    def connectNodes(self):
        for i in self.nodes: #clear the connections
            i.outputConnections.clear() 
        for i in self.genes: #for each Gene 
            i.fromNode.outputConnections.append(i) #add it to node

    #feeding in input values into the NN and returning output array
    def feedForward(self, inputValues):
        #set the outputs of the input nodes
        for i in range(self.inputs):
            self.nodes[i].outputValue = inputValues[i]
        self.nodes[self.biasNode].outputValue = 1 #output of bias is 1
        for i in self.network: #for each node in the network engage it(see node class for what this does)
            i.engage()

        #the outputs are nodes[inputs] to nodes [inputs+outputs-1]
        outs = [self.outputs]
        for i in range(self.outputs):
            outs[i] = self.nodes[self.inputs + i].outputValue
        for i in self.nodes: #reset all the nodes for the next feed forward
            i.inputSum = 0
        return outs

    #sets up the NN as a list of nodes in order to be engaged 
    def generateNetwork(self):
        self.connectNodes()
        self.network = []
        #for each layer add the node in that layer, since layers cannot connect to themselves there is no need to order the nodes within a layer
        for l in self.layers: #for each layer
            for i in self.nodes: #for each node
                if i.layer == l: #if that node is in that layer
                    self.network.append(i)

    #mutate the NN by adding a new node
    #it does this by picking a random connection and disabling it then 2 new connections are added 
    #1 between the input node of the disabled connection and the new node
    #and the other between the new node and the output of the disabled connection
    def addNode(self, innovationHistory):
        #pick a random connection to create a node between
        if len(self.genes) == 0:
            self.addConnection(innovationHistory)
            return
        randomConnection = math.floor(random.randint(1, len(self.genes)))
        
        while self.genes[randomConnection].fromNode == self.nodes[self.biasNode] and len(self.genes) !=1 : #dont disconnect bias
            randomConnection = math.floor(random.randint(1, len(self.genes)))

        self.genes[randomConnection].enabled = False #disable it
        newNodeNo = self.nextNode
        self.nodes.append(Node(newNodeNo))
        self.nextNode += 1

        #add a new connection to the new node with a weight of 1
        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.genes[randomConnection].fromNode, self.getNode(newNodeNo))
        self.genes.append(Gene(self.genes[randomConnection].fromNode, self.getNode(newNodeNo), 1, connectionInnovationNumber))
        
        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.getNode(newNodeNo), self.genes[randomConnection].toNode) #fix this
        #add a new connection from the new node with a weight the same as the disabled connection
        self.genes.append(Gene(self.getNode(newNodeNo), self.genes[randomConnection].toNode, self.genes[randomConnection].weight, connectionInnovationNumber))
        self.getNode(newNodeNo).layer = self.genes[randomConnection].fromNode.layer + 1
        
        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.biasNode, self.getNode(newNodeNo))
        #connect the bias to the new node with a weight of 0 
        self.genes.append(Gene(self.nodes[self.biasNode], self.getNode(newNodeNo), 0, connectionInnovationNumber))
        
        #if the layer of the new node is equal to the layer of the output node of the old connection then a new layer needs to be created
        #more accurately the layer numbers of all layers equal to or greater than this new node need to be incrimented
        if self.getNode(newNodeNo).layer == self.genes[randomConnection].toNode.layer:
            for i in self.nodes: #dont include this newest node
                if i.layer >= self.getNode(newNodeNo).layer:
                    i.layer += 1
            self.layers += 1
        self.connectNodes()

    #adds a connection between 2 nodes which aren't currently connected
    def addConnection(self, innovationHistory):
        #cannot add a connection to a fully connected network
        if self.fullyConnected():
            print("connection failed")
            return

        #get random nodes
        randomNode1 = math.floor(random.randint(1, len(self.nodes))) 
        randomNode2 = math.floor(random.randint(1, len(self.nodes))) 
        while self.randomConnectionNodesAreBad(randomNode1, randomNode2): 
            #while the random nodes are no good, get new ones
            randomNode1 = math.floor(random.randint(1, len(self.nodes))) 
            randomNode2 = math.floor(random.randint(1, len(self.nodes)))

        temp = 0

        if self.nodes[randomNode1].layer > self.nodes[randomNode2].layer: 
            #if the first random node is after the second then switch
            temp = randomNode2
            randomNode2 = randomNode1
            randomNode1 = temp

        #get the innovation number of the connection
        #this will be a new number if no identical genome has mutated in the same way 
        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.nodes[randomNode1], self.nodes[randomNode2])
        
        #add the connection with a random array
        self.genes.append(Gene(self.nodes[randomNode1], self.nodes[randomNode2], random.random(-1, 1), connectionInnovationNumber))
        self.connectNodes()

    def randomConnectionNodesAreBad(self, r1, r2):
        if self.nodes[r1].layer == self.nodes[r2].layer:
            return True #if the nodes are in the same layer 
        if self.nodes[r1].isConnectedTo(self.nodes[r2]): 
            return True #if the nodes are already connected
        return False

    #returns the innovation number for the new mutation
    #if this mutation has never been seen before then it will be given a new unique innovation number
    #if this mutation matches a previous mutation then it will be given the same innovation number as the previous one
    def getInnovationNumber(self, innovationHistory, fromNode, toNode):
        isNew = True
        connectionInnovationNumber = self.nextConnectionNo
        for i in innovationHistory: #for each previous mutation
            if i.matches(self, fromNode, toNode): #if match found
                isNew = False #its not a new mutation
                #set the innovation number as the innovation number of the match
                connectionInnovationNumber = innovationHistory[i].innovationNumber 
                break
        if isNew: #if the mutation is new then create an arrayList of integers representing the current state of the genome
            innoNumbers = []
            for i in self.genes: #set the innovation numbers
                innoNumbers.append(i.innovationNo)
        #then add this mutation to the innovationHistory 
        innovationHistory.append(connectionHistory(fromNode.number, toNode.number, connectionInnovationNumber, innoNumbers))
        self.nextConnectionNo += 1
        return connectionInnovationNumber

    #returns whether the network is fully connected or not
    def fullyConnected(self):
        maxConnections = 0
        nodesInLayers = [self.layers] #array which stored the amount of nodes in each layer
        
        #populate array
        for i in self.nodes:
            nodesInLayers[i.layer] += 1

        #for each layer the maximum amount of connections is the number in this layer * the number of nodes infront of it
        #so lets add the max for each layer together and then we will get the maximum amount of connections in the network
        for i in range(self.layers):
            nodesInFront = 0
            for j in range(self.layers): #for each layer infront of this layer
                nodesInFront += nodesInLayers[j] #add up nodes
            maxConnections += nodesInLayers[i] * nodesInFront
        
        if maxConnections == (len(self.genes)): 
            #if the number of connections is equal to the max number of connections possible then it is full
            return True
        return False

    # mutates the genome
    def mutate(self, innovationHistory):
        if len(self.genes) == 0:
            self.addConnection(innovationHistory)

        rand1 = random.random(1)
        if rand1 < 0.8: # 80% of the time mutate weights
            for i in range(len(self.genes)):
                self.genes[i].mutateWeight()

        # 8% of the time add a new connection
        rand2 = random.random(1)
        if rand2 < 0.08:
            self.addConnection(innovationHistory)
            
        # 2% of the time add a node
        rand3 = random.random(1)
        if rand3 < 0.02:
            self.addNode(innovationHistory)

    #called when this Genome is better that the other parent
    def crossover(self, parent2):
        child = NeuralNet(self.inputs, self.outputs)
        child.genes.clear()
        child.nodes.clear()
        child.layers = self.layers
        child.nextNode = self.nextNode
        child.biasNode = self.biasNode
        childGenes = [] #list of genes to be inherrited form the parents
        isEnabled = [] 

        #all inherited genes
        for i in range(len(self.genes)):
            setEnabled = True #is this node in the chlid going to be enabled

            parent2gene = self.matchingGene(parent2, self.genes[i].innovationNo)
            if parent2gene != -1: #if the genes match
                if not self.genes[i].enabled or not parent2.genes[parent2gene].enabled: 
                    #if either of the matching genes are disabled
                    if random.random(1) < 0.75: #75% of the time disabel the childs gene
                        setEnabled = False
                rand = random.random(1)
                if rand<0.5 :
                    childGenes.append(self.genes[i])
                    #get gene
                else:
                    #get gene from parent2
                    childGenes.append(parent2.genes[parent2gene])
            else: #disjoint or excess gene
                childGenes.append(self.genes[i])
                setEnabled = self.genes[i].enabled
            isEnabled.append(setEnabled)

        #since all excess and disjoint genes are inherrited from the more fit parent (this Genome) 
        # the childs structure is no different from this parent | with exception of dormant connections 
        # being enabled but this wont effect nodes so all the nodes can be inherrited from this parent
        for i in range(len(self.nodes)):
            child.nodes.append(self.nodes[i].clone())

        #clone all the connections so that they connect the childs new nodes
        for i in range(len(childGenes)):
            child.genes.append(childGenes[i].clone(child.getNode(childGenes[i].fromNode.number), child.getNode(childGenes[i].toNode.number)))
            child.genes[i].enabled = isEnabled[i]
        child.connectNodes()
        return child
    """
    # create an empty genome
    def __init__(self,inputs,outputs):
        #set input number and output number
        self.inputs = inputs 
        self.outputs = outputs
    """
    # returns whether or not there is a gene matching the input innovation number  in the input genome
    def matchingGene(self, parent2, innovationNumber):
        for i in self.genes:
            if i.innovationNo == innovationNumber:
                return i
        return -1 #no matching gene found

    """
    #prints out info about the genome to the console 
    def printGenome(self):
        print("Print genome  layers:", self.layers, "\n")
        print ("bias node: ", self.biasNode, "\n")
        print("nodes\n")
        for i in range(len(self.nodes)):
            print(self.nodes[i].number, ",")
        print("\nGenes\n")
        for i in range(len(self.genes)): #for each connectionGene 
            print("gene ", self.genes[i].innovationNo, "From node ", self.genes[i].fromNode.number, "To node ", self.genes[i].toNode.number, "is enabled ", self.genes.[i].enabled, "from layer ", self.genes[i].fromNode.layer, "to layer ", self.genes[i].toNode.layer, "weight: ", self.genes[i].weight, "\n")
        print("\n")
    """
    # returns a copy of this genome
    def clone(self):
        clone = NeuralNet(self.inputs, self.outputs)
        for i in self.nodes: # copy nodes
            clone.nodes.append(i.clone())
        
        #copy all the connections so that they connect the clone new nodes
        for i in self.genes: # copy genes
            clone.genes.append(i.clone(clone.getNode(i.fromNode.number), clone.getNode(i.toNode.number)))

        clone.layers = self.layers
        clone.nextNode = self.nextNode
        clone.biasNode = self.biasNode
        clone.connectNodes()
        return clone


