from Player import *
from Game import *
from Species import *
class Population():

#------------------------------------------------------------------------------------------------------------------------------------------
    #constructor
    def __init__(self,size, screen):
        self.games = []
        self.bestPlayer = None
        self.bestScore = 0
        self.gen = 0
        self.innovationHistory = []
        self.genPlayers = []
        self.species = []
        self.screen = screen

        self.massExtinctionEvent = False
        self.newStage = False
        self.populationLife = 0
        for i in range(size):
            self.games.append(Game(screen))
            self.games[i].player.brain.generateNetwork()
            self.games[i].player.brain.mutate(self.innovationHistory)

#------------------------------------------------------------------------------------------------------------------------------------------
    #update all the players which are alive
    # def updateAlive(self):
    #     self.populationLife += 1
    #     for i in self.pop:
    #         if not i.isDead:
    #             i.look() # get inputs for brain 
    #             i.think() # use outputs from neural network
    #             i.update() # move the player according to the outputs from the neural network
    #             if not i.showNothing:
    #                 self.pop[i].show()

#------------------------------------------------------------------------------------------------------------------------------------------ 
    # #returns true if all the players are dead      sad
    # def done(self):
    #     for i in range(len(self.pop)):
    #         if not self.pop[i].isDead:
    #             return False
    #     return True

#------------------------------------------------------------------------------------------------------------------------------------------
    #sets the best player globally and for this gen
    def setBestPlayer(self):
        #tempBest =  Species.selectPlayer(0) 
        if len(self.genPlayers) > 0:
            tempBest =  self.genPlayers[0]
            tempBest.gen = self.gen
            
            #if best this gen is better than the global best score then set the global best as the best this gen
            if tempBest.score > self.bestScore:
                self.genPlayers.append(tempBest.cloneForReplay())
                print("old best:", self.bestScore,"\n")
                print("new best:", tempBest.score,"\n")
                self.bestScore = tempBest.score
                self.bestPlayer = tempBest.cloneForReplay()

#------------------------------------------------------------------------------------------------------------------------------------------------
    # this function is called when all the players in the population are dead and a new generation needs to be made
    def naturalSelection(self):
        self.speciate() #seperate the population into species 
        self.calculateFitness() #calculate the fitness of each player
        self.sortSpecies() #sort the species to be ranked in fitness order, best first
        if self.massExtinctionEvent:
            self.massExtinction()
            self.massExtinctionEvent = False

        self.cullSpecies() # kill off the bottom half of each species
        self.setBestPlayer() # save the best player of this gen
        self.killStaleSpecies() # remove species which haven't improved in the last 15(ish) generations
        self.killBadSpecies() # kill species which are so bad that they cant reproduce
        
        print("generation", self.gen, "Number of mutations", len(self.innovationHistory), 
            "species: ", len(self.species), "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        
        averageSum = self.getAvgFitnessSum()
        children = [] #the next generation

        print("Species:\n")              
        for j in range(len(self.species)): #for each species
            print("best unadjusted fitness:", self.species[j].bestFitness)
            for i in range(len(self.species[j].players)):
                print("player ", i, "fitness: ", self.species[j].players[i].fitness, ' ')
            print("\n")
            
            children.append(self.species[j].champ.clone()) #add champion without any mutation
            NoOfChildren = math.floor(self.species[j].averageFitness / averageSum * len(self.games)) -1 # the number of children this species is allowed, note -1 is because the champ is already added
            for i in range(NoOfChildren): #get the calculated amount of children from this species
                children.append(self.species[j].giveMeBaby(self.innovationHistory))
            
        while len(children) < len(self.games): #if not enough babies (due to flooring the number of children to get a whole int) 
            children.append(self.species[0].giveMeBaby(self.innovationHistory)) #get babies from the best species
        self.games.clear()

        for child in children: #set the children as the current population
            self.games.append(Game(self.screen, child))
        #self.games = children[:] #set the children as the current population

        
        self.gen += 1 
        for game in self.games: # generate networks for each of the children
            game.player.brain.generateNetwork()
        populationLife = 0

#------------------------------------------------------------------------------------------------------------------------------------------
    #seperate population into species based on how similar they are to the leaders of each species in the previous gen
    def speciate(self):
        for s in self.species: #empty species
            s.players.clear()
        for game in self.games: # for each player
            speciesFound = False
            for s in self.species: # for each species
                if s.sameSpecies(game.player.brain): # if the player is similar enough to be considered in the same species
                    s.addToSpecies(game.player) # add it to the species
                    speciesFound = True
                    break
            if not speciesFound: # if no species was similar enough then add a new species with this as its champion
                self.species.append(Species(game.player))

#------------------------------------------------------------------------------------------------------------------------------------------
    #calculates the fitness of all of the players 
    def calculateFitness(self):
        for game in self.games:
            game.player.calculateFitness()

#------------------------------------------------------------------------------------------------------------------------------------------
    #sorts the players within a species and the species by their fitnesses
    def sortSpecies(self):
        # sort the players within a species
        for s in self.species:
            s.sortSpecies()
        
        # sort the species by the fitness of its best player
        # using selection sort like a loser
        temp = []
        for i in self.species:
            maxScore = 0.0
            maxIndex = 0
            for j in range(len(self.species)): 
                if self.species[j].bestFitness > maxScore:
                    maxScore = self.species[j].bestFitness
                    maxIndex = j
            temp.append(self.species[maxIndex])
            self.species.pop(maxIndex)
        self.species = temp[:]

#------------------------------------------------------------------------------------------------------------------------------------------
    #kills all species which haven't improved in 15 generations
    def killStaleSpecies(self):
        for i in range(2,len(self.species)):
            if self.species[i].staleness >= 15:
                self.species.remove(i)
                i -= 1

#------------------------------------------------------------------------------------------------------------------------------------------
    #if a species sucks so much that it wont even be allocated 1 child for the next generation then kill it now
    def killBadSpecies(self):
        averageSum = self.getAvgFitnessSum()
        for i in self.species:
            if i.averageFitness / averageSum * len(self.games) < 1: #if wont be given a single child 
                self.species.remove(i) # sad
                i -= 1

#------------------------------------------------------------------------------------------------------------------------------------------
    # returns the sum of each species average fitness
    def getAvgFitnessSum(self):
        averageSum = 0
        for s in self.species:
            averageSum += s.averageFitness
        return averageSum

#------------------------------------------------------------------------------------------------------------------------------------------
    # kill the bottom half of each species
    def cullSpecies(self):
        for s in self.species:
            s.cull() # kill bottom half
            s.fitnessSharing() # also while we're at it lets do fitness sharing
            s.setAverage() # reset averages because they will have changed

    def massExtinction(self):
        for i in range(5, len(self.species)):
                self.species.pop(i) #sad
                i -= 1
    
    def draw(self, showNothing, showIndex):
        if not showNothing:
            if showIndex == -1: #showAll
                self.games[0].level.drawBG(self.games[0])
                for game in self.games:
                    game.level.draw() #draw elements
            else: #use index - show only that game
                self.games[showIndex].level.drawBG(self.games[showIndex])
                self.games[showIndex].level.draw()
