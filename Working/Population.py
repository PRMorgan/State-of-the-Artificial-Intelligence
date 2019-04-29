from Player import *
from Game import *
from Species import *
import math

class Population():

   #construct the population
    def __init__(self,size, screen):
        self.games = []
        #self.bestPlayer = None
        self.bestScore = -1000
        self.gen = 0
        self.innovationHistory = []
        #self.genPlayers = []
        self.species = []
        self.screen = screen

        self.massExtinctionEvent = False
        self.newStage = False
        self.populationLife = 0

        #Add the brains to each player
        for i in range(size):
            self.games.append(Game(screen))
            self.games[i].player.brain.generateNetwork()
            #Mutate those brains
            self.games[i].player.brain.mutate(self.innovationHistory)
            self.games[i].player.brain.mutate(self.innovationHistory)

    #sets the best player globally and for this gen
    def setBestPlayer(self):
        # tempBest = self.games[0]
        # tempBest.gen = self.gen
        # for game in self.games:
        #     if game.player.fitness > tempBest.player.fitness:
        #         tempBest = game
        # if tempBest.player.fitness > self.bestScore:
        #     #self.genPlayers.append(tempBest.player.clone())
        #     print("old best:", self.bestScore,"\n")
        #     print("new best:", tempBest.player.fitness,"\n")
        self.bestScore = self.species[0].bestFitness
            #self.bestPlayer = tempBest.player.clone()

    # this function is called when all the players in the population are dead and a new generation needs to be made
    def naturalSelection(self):
        self.calculateFitness() #calculate the fitness of each player
        self.speciate() #seperate the population into species 
        self.sortSpecies() #sort the species to be ranked in fitness order, best first
        if self.massExtinctionEvent:
            self.massExtinction()
            self.massExtinctionEvent = False

        self.cullSpecies() # kill off the bottom half of each species
        self.setBestPlayer() # save the best player of this gen
        self.killStaleSpecies() # remove species which haven't improved in the last 15(ish) generations
        self.killBadSpecies() # kill species which are so bad that they cant reproduce
        
        print("generation", self.gen, "Number of mutations", len(self.innovationHistory), 
            "species: ", len(self.species), "<<<<<\n")
        
        self.calculateFitness() #calculate the fitness of each player
        averageSum = self.getAvgFitnessSum()
        children = [] #the next generation

        print("Species:\n")              
        for species in self.species: #for each species
            print("best unadjusted fitness:", species.bestFitness)
            for i in range(len(species.players)):
                print("player ", i, "fitness: ", species.players[i].fitness, ' ')
            print("\n")
            children.append(species.champ.clone()) #add champion without any mutation
            NoOfChildren = math.floor(species.averageFitness / averageSum * len(self.games)) -1 # the number of children this species is allowed, note -1 is because the champ is already added
            for i in range(NoOfChildren): #get the calculated amount of children from this species
                children.append(species.giveMeBaby(self.innovationHistory))
            
        while len(children) < len(self.games): #if not enough babies (due to flooring the number of children to get a whole int) 
            children.append(self.species[0].giveMeBaby(self.innovationHistory)) #get babies from the best species

        self.games.clear()

        for child in children: #set the children as the current population
            self.games.append(Game(self.screen, child))

        self.resetFitness()
        self.gen += 1
        # for game in self.games: # generate networks for each of the children
        #     game.player.brain.generateNetwork()

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

    #calculates the fitness of all of the players 
    def calculateFitness(self):
        for game in self.games:
            game.player.calculateFitness()

    #sorts the players within a species and the species by their fitnesses
    def sortSpecies(self):
        # sort the players within a species
        for s in self.species:
            s.sortSpecies()
        self.species = self.merge_sort(self.species)

    #kills all species which haven't improved in 15 generations
    def killStaleSpecies(self):
        i = 2
        while i < len(self.species):
            if self.species[i].staleness >= 15:
                self.species.pop(i)
            else:
                i += 1

    #if a species sucks so much that it wont even be allocated 1 child for the next generation then kill it now
    def killBadSpecies(self):
        averageSum = self.getAvgFitnessSum()
        i = 0
        while i < len(self.species):
            if self.species[i].averageFitness / averageSum * len(self.games) < 1: #if wont be given a single child 
                self.species.pop(i) # sad
            else: 
                i += 1

    # returns the sum of each species average fitness
    def getAvgFitnessSum(self):
        averageSum = 0
        for s in self.species:
            averageSum += s.averageFitness
        return averageSum

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
                self.games[0].player.brain.draw(self.screen, self.gen)
                for game in self.games:
                    game.level.draw(game) #draw elements
            else: #use index - show only that game
                self.games[showIndex].level.drawBG(self.games[showIndex])
                self.games[showIndex].level.draw(self.games[showIndex])
                self.games[showIndex].player.brain.draw(self.screen, self.gen)

    def resetFitness(self):
        for game in self.games:
            game.player.resetFitness()

    # merge sort algorithm
    #https://medium.com/@george.seif94/a-tour-of-the-top-5-sorting-algorithms-with-python-code-43ea9aa02889
    def merge_sort(self, arr):
        # The last array split
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        # Perform merge_sort recursively on both halves
        left, right = self.merge_sort(arr[:mid]), self.merge_sort(arr[mid:])
        # Merge each side together
        return self.merge(left, right, arr.copy())


    def merge(self, left, right, merged):
        left_cursor, right_cursor = 0, 0
        while left_cursor < len(left) and right_cursor < len(right):
        
            # Sort each one and place into the result
            if left[left_cursor].bestFitness >= right[right_cursor].bestFitness:
                merged[left_cursor+right_cursor]=left[left_cursor]
                left_cursor += 1
            else:
                merged[left_cursor + right_cursor] = right[right_cursor]
                right_cursor += 1
                
        for left_cursor in range(left_cursor, len(left)):
            merged[left_cursor + right_cursor] = left[left_cursor]
            
        for right_cursor in range(right_cursor, len(right)):
            merged[left_cursor + right_cursor] = right[right_cursor]

        return merged