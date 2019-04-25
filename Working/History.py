class connectionHistory():
#--------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #constructor
    def __init__(self, fromNode, toNode,inno,innovationNos):
        self.fromNode = fromNode
        self.toNode = toNode
        self.innovationNumber = inno
        self.innovationNumbers = innovationNos[:]
        # the innovation Numbers from the connections of the genome which first had this mutation 
        # this represents the genome and allows us to test if another genoeme is the same
        # this is before this connection was added

#---------------------------------------------------------------------------------------------------------------------------------------------------------
    #returns whether the genome matches the original genome and the connection is between the same nodes
    def matches(self, genome, fromNode, toNode):
        if len(genome.genes) == len(self.innovationNumbers): #if the number of connections are different then the genoemes aren't the same
            if fromNode.number == self.fromNode and toNode.number == self.toNode:
                #next check if all the innovation numbers match from the genome
                for gene in genome.genes:
                    if gene.innovationNumber not in self.innovationNumbers:
                        return False
                #if reached this far then the innovationNumbers match the genes innovation numbers 
                # and the connection is between the same nodes so it does match
                return True
        return False