import random

class Species():
#--------------------------------------------
    # coefficients for testing compatibility 
    excessCoeff = 1.0
    weightDiffCoeff = 0.5
    compatibilityThreshold = 3.0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # constructor which takes in the player which belongs to the species
    def __init__(self, p = 0):
        self.players = []
        self.players.append(p) 
        #since it is the only one in the species it is by default the best
        self.bestFitness = p.fitness
        self.rep = p.brain.clone()
        self.champ = p.cloneForReplay()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # returns whether the parameter genome is in this species
    def sameSpecies(self, g):
        compatibility = 0.0
        excessAndDisjoint = self.getExcessDisjoint(g, self.rep) # get the number of excess and disjoint genes between this player and the current species rep
        averageWeightDiff = self.averageWeightDiff(g, self.rep) # get the average weight difference between matching genes
        
        largeGenomeNormalizer = len(g.genes) - 20
        if largeGenomeNormalizer < 1:
            largeGenomeNormalizer =1

        compatibility =  (self.excessCoeff* excessAndDisjoint / largeGenomeNormalizer) + (self.weightDiffCoeff* averageWeightDiff) #compatablilty formula
        return self.compatibilityThreshold > compatibility

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #add a player to the species
    def addToSpecies(self, p):
        self.players.append(p)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #returns the number of excess and disjoint genes between the 2 input genomes
    #i.e. returns the number of genes which dont match
    def getExcessDisjoint(self, brain1, brain2):
        matching = 0.0
        for i in range(len(brain1.genes)):
            for j in brain2.genes:
                if i.innovationNo == brain2.genes[j].innovationNo:
                    matching += 1
                    break
        return len(brain1.genes) + len(brain2.genes) - 2 * (matching) # return no of excess and disjoint genes

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #returns the avereage weight difference between matching genes in the input genomes
    def averageWeightDiff(self, brain1, brain2):
        if len(brain1.genes) == 0 or len(brain2.genes) ==0:
            return 0

        matching = 0.0
        totalDiff= 0.0
        for i in range(len(brain1.genes)):
            for j in range(len(brain2.genes)):
                if brain1.genes[i].innovationNo == brain2.genes[j].innovationNo:
                    matching += 1
                    totalDiff += abs(brain1.genes[i].weight - brain2.genes[j].weight)
                    break
        if matching ==0: # divide by 0 error
            return 100
        return totalDiff / matching

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # sorts the species by fitness 
    def sortSpecies(self):
        temp = []
        
        #selection short 
        for i in range(len(self.players)):
            maxScore = 0.0
            maxIndex = 0
            for j in range(len(self.players)):
                if self.players[j].fitness > maxScore:
                    maxScore = self.players[j].fitness
                    maxIndex = j

            temp.append(self.players[maxIndex])
            self.players.remove(maxIndex)
            i -= 1
        self.players = temp[:]
        if len(self.players) == 0:
            self.staleness = 200
            return
        # if new best player
        if self.players[0].fitness > self.bestFitness:
            self.staleness = 0
            self.bestFitness = self.players[0].fitness
            self.rep = self.players[0].brain.clone()
            self.champ = self.players[0].cloneForReplay()
        else: # if no new best player
            self.staleness += 1

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #simple stuff
    def setAverage(self):
        sumScores = 0.0
        for i in range(len(self.players)):
            sumScores += self.players[i].fitness
        self. averageFitness = sumScores / len(self.players)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # gets baby from the players in this species
    def giveMeBaby(self, innovationHistory):
        baby = None
        if random.random(1) < 0.25: # 25% of the time there is no crossover and the child is simply a clone of a random(ish) player
            baby = self.selectPlayer().clone()
        else: # 75% of the time do crossover 
            # get 2 random(ish) parents 
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()
            
            #the crossover function expects the highest fitness parent to be the object and the lowest as the argument
            if parent1.fitness < parent2.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby =  parent1.crossover(parent2)
        baby.brain.mutate(innovationHistory) # mutate that baby brain
        return baby

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # selects a player based on it fitness
    def selectPlayer(self):
        fitnessSum = 0.0
        for i in range(len(self.players)):
            fitnessSum += self.players[i].fitness
        
        rand = random.random(fitnessSum)
        runningSum = 0.0

        for i in range(len(self.players)):
            runningSum += self.players[i].fitness 
            if runningSum > rand:
                return self.players[i]

        # unreachable code to make the parser happy
        return self.players[0]

#------------------------------------------------------------------------------------------------------------------------------------------
    #kills off bottom half of the species
    def cull(self):
        if len(self.players) > 2:
            for i in range(len(self.players)/2, len(self.players)):
                self.players.remove(i)
                i -= 1

#------------------------------------------------------------------------------------------------------------------------------------------
    #in order to protect unique players, the fitnesses of each player is divided by the number of players in the species that that player belongs to 
    def fitnessSharing(self):
        for i in range(len(self.players)):
            self.players[i].fitness /= len(self.players)