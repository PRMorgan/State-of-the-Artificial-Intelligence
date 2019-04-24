import random 

#a connection between 2 nodes
class Gene():
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #constructor
    def __init__(self, fromNode, toNode, w, inno):
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = w
        self.innovationNo = inno #each connection is given a innovation number to compare genomes
        self.enabled = True
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #changes the weight
    def mutateWeight(self):
        rand2 = random.random(1)
        if rand2 < 0.1: #10% of the time completely change the weight
           self.weight = random.random(-1, 1)
        else: #otherwise slightly change it
            self.weight += random.randrange(1, 200)/50 #What is this and how to fix??
            #keep weight between bounds
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1     
#----------------------------------------------------------------------------------------------------------
    #returns a copy of this connectionGene
    def clone(self,fromNode,toNode):
        clone = Gene(self.fromNode, self.toNode, self.weight, self.innovationNo)
        clone.enabled = self.enabled
        return clone