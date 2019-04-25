# AI-Kido

AI-Kido is an NPC vs NPC fighter game implemented using the Python programming language and the Pygame library. This program was written for the CS 480 - Artificial Intelligence class at Truman State University.

Contributors:
* Gabe Lewis
* Garrett Money
* Patrick Morgan
* Rebecca Niemeier

## Basic Explanation

AI-Kido is a figthing game in which we pit two computer players against one another. One NPC is implemented using random event generation while the other player is implemented using a nueral net and genetic algorithm.

## Thorough Explanation

We are taking the NEAT (NeuroEvolutionary Augmented Topologies) approach. The way this algorithm will fit in with our game is similar to most games that NEAT is implemented in. There are a few crucial parts that are consistent with all implementations of NEAT, the fact that the agent is controlled by a neural network and that the neural network is modified by a genetic algorithm.

Our implementation is a game structure. This includes 2D physics and a game environment that supports players moving around. Our driver class (AI-Kido.py) will create a set of games (50 or so). These games will contain two players each, that start on opposite sides. These two enemies are contained within their own copy of a generic level that we created for all players to interact. Each player is controlled with a neural net defined within a “Genome.” The players look (take inputs into input nodes), think (forward propagates and determines outputs), and act (takes the last layer of output nodes and tells the players to act depending on which ones are active). 

Once one player wins by getting to the opposite side sa many times as possible before the timer runs out (60 seconds), the players will be evaluated on their fitness level. It is at this point we run through the normal genetic algorithm involving: selection, crossover, and mutation. The players will fight previous (best) versions of themselves as they mutate to train. After numerous levels, our AI will have gained knowledge and will be able to beat previous versions of itself as well as put up a decent fight against itself.

## Running the Program

1) Download Working directory
2) Run AI-Kido.py
