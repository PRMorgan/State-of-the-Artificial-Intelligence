import random

class NeuralNet:
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,inputs,outputs):
        #set input number and output number
        self.inputs = inputs
        self.outputs = outputs
        self.layers = 2
        self.nextNode = 0
        self.biasNode = 0
        self.nodes = [] #list of nodes
        self.genes = [] #list of connections between nodes which represent the NN
        self.network = [] #list of the nodes in the order that they need to be considered in the NN

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
        self.nodes.append(Node(nextNode)) #bias node
        self.biasNode = nextNode
        self.nextNode += 1
        self.nodes[biasNode].layer = 0

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #returns the node with a matching number
    #sometimes the nodes will not be in order
    def getNode(self,nodeNumber):
        for i in range(len(self.nodes)):
            if nodes[i].number == self.nodeNumber:
                return nodes[i]
        return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #adds the conenctions going out of a node to that node so that it can acess the next node during feeding forward
    def connectNodes(self):
        for i in range(len(self.nodes)): #clear the connections
            nodes[i].outputConnections.clear()
        for i in range(len(self.genes)): #for each Gene 
            self.genes[i].fromNode.outputConnections.append(genes[i]) #add it to node

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #feeding in input values into the NN and returning output array
    def feedForward(self, inputValues):
        #set the outputs of the input nodes
        for i in range(self.inputs):
            self.nodes[i].outputValue = inputValues[i]
        self.nodes[self.biasNode].outputValue = 1 #output of bias is 1
        for i in range(len(self.network)): #for each node in the network engage it(see node class for what this does)
            self.network[i].engage()

        #the outputs are nodes[inputs] to nodes [inputs+outputs-1]
        outs = [self.outputs]
        for i in range(self.outputs):
            outs[i] = self.nodes[inputs + i].outputValue
        for i in range(len(self.nodes)): #reset all the nodes for the next feed forward
            self.nodes[i].inputSum = 0
        return outs

#----------------------------------------------------------------------------------------------------------------------------------------
    #sets up the NN as a list of nodes in order to be engaged 
    def generateNetwork(self):
        connectNodes()
        self.network = []
        #for each layer add the node in that layer, since layers cannot connect to themselves there is no need to order the nodes within a layer
        for l in range(self.layers): #for each layer
            for i in range(len(self.nodes)): #for each node
                if self.nodes[i].layer == l: #if that node is in that layer
                    self.network.append(nodes[i])

#-----------------------------------------------------------------------------------------------------------------------------------------
    #mutate the NN by adding a new node
    #it does this by picking a random connection and disabling it then 2 new connections are added 
    #1 between the input node of the disabled connection and the new node
    #and the other between the new node and the output of the disabled connection
    def addNode(self, innovationHistory):
        #pick a random connection to create a node between
        if len(self.genes) == 0:
            addConnection(innovationHistory)
            return
        randomConnection = math.floor(random(len(self.genes)))
        
        while self.genes[randomConnection].fromNode == self.nodes[biasNode] and len(self.genes) !=1 : #dont disconnect bias
            randomConnection = math.floor(random(len(self.genes)))
        self.genes[randomConnection].enabled = False #disable it
        newNodeNo = self.nextNode
        self.nodes.append(Node(newNodeNo))
        nextNode += 1
        #add a new connection to the new node with a weight of 1
        connectionInnovationNumber = getInnovationNumber(innovationHistory, self.genes[randomConnection].fromNode, getNode(newNodeNo))
        self.genes.append(Gene(self.genes[randomConnection].fromNode, getNode(newNodeNo), 1, connectionInnovationNumber))
        
        connectionInnovationNumber = getInnovationNumber(innovationHistory, getNode(newNodeNo), self.genes.get(randomConnection).toNode)
        #add a new connection from the new node with a weight the same as the disabled connection
        self.genes.append(Gene(getNode(newNodeNo), self.genes[randomConnection].toNode, self.genes[randomConnection].weight, connectionInnovationNumber))
        getNode(newNodeNo).layer = self.genes[randomConnection].fromNode.layer + 1
        
        connectionInnovationNumber = getInnovationNumber(innovationHistory, self.nodes.get(self.biasNode), self.getNode(newNodeNo));
        #connect the bias to the new node with a weight of 0 
        self.genes.append(Gene(self.nodes[biasNode], getNode(newNodeNo), 0, connectionInnovationNumber))
        #if the layer of the new node is equal to the layer of the output node of the old connection then a new layer needs to be created
        #more accurately the layer numbers of all layers equal to or greater than this new node need to be incrimented
        if getNode(newNodeNo).layer == self.genes[randomConnection].toNode.layer:
            for i in range(len(self.nodes)): #dont include this newest node
                if self.nodes[i].layer >= getNode(newNodeNo).layer:
                    self.nodes[i].layer += 1
            layers += 1
        connectNodes()

#------------------------------------------------------------------------------------------------------------------
    #adds a connection between 2 nodes which aren't currently connected
    def addConnection(self, innovationHistory):
        #cannot add a connection to a fully connected network
        if fullyConnected():
            print("connection failed")
            return
        #get random nodes
        randomNode1 = math.floor(random(len(self.nodes))) 
        randomNode2 = math.floor(random(len(self.nodes))) 
        while randomConnectionNodesAreBad(randomNode1, randomNode2): 
            #while the random nodes are no good, get new ones
            randomNode1 = math.floor(random(len(self.nodes))) 
            randomNode2 = math.floor(random(len(self.nodes)))
        temp = 0
        if self.nodes[randomNode1].layer > self.nodes[randomNode2].layer: 
            #if the first random node is after the second then switch
            temp = randomNode2
            randomNode2 = randomNode1
            randomNode1 = temp

        #get the innovation number of the connection
        #this will be a new number if no identical genome has mutated in the same way 
        connectionInnovationNumber = getInnovationNumber(innovationHistory, self.nodes[randomNode1], self.nodes[randomNode2])
        #add the connection with a random array
        self.genes.append(Gene(self.nodes[randomNode1], self.nodes[randomNode2], random(-1, 1), connectionInnovationNumber))
        connectNodes()

#-------------------------------------------------------------------------------------------------------------------------------------------
    def randomConnectionNodesAreBad(self, r1, r2):
        if self.nodes[r1].layer == self.nodes[r2].layer:
            return True #if the nodes are in the same layer 
        if self.nodes[r1].isConnectedTo(self.nodes[r2]): 
            return True #if the nodes are already connected
        return False

#-------------------------------------------------------------------------------------------------------------------------------------------
    #returns the innovation number for the new mutation
    #if this mutation has never been seen before then it will be given a new unique innovation number
    #if this mutation matches a previous mutation then it will be given the same innovation number as the previous one
    def getInnovationNumber(self, innovationHistory, fromNode, toNode):
        isNew = True
        connectionInnovationNumber = nextConnectionNo
        for i in range(len(innovationHistory)): #for each previous mutation
            if innovationHistory[i].matches(self, fromNode, toNode): #if match found
                isNew = False #its not a new mutation
                #set the innovation number as the innovation number of the match
                connectionInnovationNumber = innovationHistory[i].innovationNumber 
                break
        if isNew: #if the mutation is new then create an arrayList of integers representing the current state of the genome
            innoNumbers = []
            for i in range(len(self.genes)): #set the innovation numbers
                innoNumbers.append(self.genes[i].innovationNo)
        #then add this mutation to the innovationHistory 
        innovationHistory.append(connectionHistory(fromNode.number, toNode.number, connectionInnovationNumber, innoNumbers))
        nextConnectionNo += 1
        return connectionInnovationNumber

#----------------------------------------------------------------------------------------------------------------------------------------
    #returns whether the network is fully connected or not
    def fullyConnected(self):
        maxConnections = 0
        nodesInLayers = [layers] #array which stored the amount of nodes in each layer
        
        #populate array
        for i in range(len(self.nodes)):
            nodesInLayers[self.nodes[i].layer] += 1

        #for each layer the maximum amount of connections is the number in this layer * the number of nodes infront of it
        #so lets add the max for each layer together and then we will get the maximum amount of connections in the network
        for i in range(self.layers):
            nodesInFront = 0
            for j in range(self.layers): #for each layer infront of this layer
                nodesInFront += nodesInLayers[j]; #add up nodes
            maxConnections += nodesInLayers[i] * nodesInFront
        
        if maxConnections == self.len(self.genes): 
            #if the number of connections is equal to the max number of connections possible then it is full
            return True
        return False

#-------------------------------------------------------------------------------------------------------------------------------
    # mutates the genome
    def mutate(self, innovationHistory):
        if len(self.genes) == 0:
            addConnection(innovationHistory)

        rand1 = random.random(1)
        if rand1 < 0.8: # 80% of the time mutate weights
            for i in range(len(self.genes)):
                self.genes[i].mutateWeight()

        # 8% of the time add a new connection
        rand2 = random.random(1)
        if rand2 < 0.08:
            addConnection(innovationHistory)
            
        # 2% of the time add a node
        rand3 = random.random(1)
        if rand3 < 0.02:
            addNode(innovationHistory)

#---------------------------------------------------------------------------------------------------------------------------------
    #called when this Genome is better that the other parent
    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)
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

            parent2gene = matchingGene(parent2, self.genes[i].innovationNo)
            if parent2gene != -1: #if the genes match
                if not self.genes[i].enabled or not parent2.genes[parent2gene].enabled: 
                    #if either of the matching genes are disabled
                    if random.random(1) < 0.75: #75% of the time disabel the childs gene
                        setEnabled = False
                rand = random.random(1);
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

#----------------------------------------------------------------------------------------------------------------------------------------
    # create an empty genome
    def __init__(self,inputs,outputs,crossover):
        #set input number and output number
        self.inputs = inputs 
        self.outputs = outputs

#----------------------------------------------------------------------------------------------------------------------------------------
    # returns whether or not there is a gene matching the input innovation number  in the input genome
    def matchingGene(self, parent2, innovationNumber):
        for i in range(len(self.genes)):
            if parent2.genes[i].innovationNo == innovationNumber:
                return i
        return -1 #no matching gene found

#----------------------------------------------------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------------------------------------------
    # returns a copy of this genome
    def clone(self):
        clone = NeuralNet(self.inputs, self.outputs, True)
        for i in range(len(self.nodes)): # copy nodes
            clone.nodes.append(sel.fnodes[i].clone())
        
        #copy all the connections so that they connect the clone new nodes
        for i in range(len(self.genes)): # copy genes
            clone.genes.append(set.genes[i].clone(clone.getNode(genes[i].fromNode.number), clone.getNode(genes[i].toNode.number)))

        clone.layers = self.layers
        clone.nextNode = self.nextNode
        clone.biasNode = self.biasNode
        clone.connectNodes()
        return clone

# #----------------------------------------------------------------------------------------------------------------------------------------
#     # draw the genome on the screen
#     def drawGenome(self, startX, startY, w, h):
#         #i know its ugly but it works (and is not that important) so I'm not going to mess with it
#         allNodes = []
#         nodePoses = []
#         nodeNumbers= []
        
#         # get the positions on the screen that each node is supposed to be in
#         # split the nodes into layers
#         for i in range(self.layers):
#             temp = []
#             for j in range(len(self.nodes)): #for each node 
#                 if self.nodes[j].layer == i: #check if it is in this layer
#                     temp.append(self.nodes[j]) #add it to this layer
#             allNodes.append(temp) #add this layer to all nodes
        
#         #for each layer add the position of the node on the screen to the node posses arraylist
#         for i in range(self.layers):
#             fill(255, 0, 0)
#       float x = startX + (float)((i)*w)/(float)(layers-1);
#       for (int j = 0; j< allNodes.get(i).size(); j++) {//for the position in the layer
#         float y = startY + ((float)(j + 1.0) * h)/(float)(allNodes.get(i).size() + 1.0);
#         nodePoses.add(new PVector(x, y));
#         nodeNumbers.add(allNodes.get(i).get(j).number);
#         if(i == layers -1){
#          println(i,j,x,y); 
          
          
#         }
#       }
#     }

#     //draw connections 
#     stroke(0);
#     strokeWeight(2);
#     for (int i = 0; i< genes.size(); i++) {
#       if (genes.get(i).enabled) {
#         stroke(0);
#       } else {
#         stroke(100);
#       }
#       PVector from;
#       PVector to;
#       from = nodePoses.get(nodeNumbers.indexOf(genes.get(i).fromNode.number));
#       to = nodePoses.get(nodeNumbers.indexOf(genes.get(i).toNode.number));
#       if (genes.get(i).weight > 0) {
#         stroke(255, 0, 0);
#       } else {
#         stroke(0, 0, 255);
#       }
#       strokeWeight(map(abs(genes.get(i).weight), 0, 1, 0, 5));
#       line(from.x, from.y, to.x, to.y);
#     }

#     //draw nodes last so they appear ontop of the connection lines
#     for (int i = 0; i < nodePoses.size(); i++) {
#       fill(255);
#       stroke(0);
#       strokeWeight(1);
#       ellipse(nodePoses.get(i).x, nodePoses.get(i).y, 20, 20);
#       textSize(10);
#       fill(0);
#       textAlign(CENTER, CENTER);


#       text(nodeNumbers.get(i), nodePoses.get(i).x, nodePoses.get(i).y);
#     }
#   }
# }