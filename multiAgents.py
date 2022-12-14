# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Actions, Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()


        ghostNear = 10000000000
        foodNear = 10000000000

        for i in newGhostStates:
            ghostDist = manhattanDistance(newPos, i.configuration.pos)
            if ghostDist == 0:
                ghostNear = min(ghostNear, ghostDist)

        if not newFood.asList():
            foodNear = 0
        else:
            for i in newFood.asList():
                foodNear = min(foodNear, manhattanDistance(i, newPos))

        good = successorGameState.getScore()
        bad = 7/(ghostNear + 1) + foodNear/3
        score = good - bad
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """


        def getMinMax(gState, dep, ag):
            des = None
            if ag == gState.getNumAgents():
                ag = 0
                dep = dep + 1
            if gState.isWin() or gState.isLose() or dep == self.depth:
                return self.evaluationFunction(gState)
            if ag == 0:
                des = [-100000000000, ""]
            else:
                des = [100000000000, ""]

            actList = gState.getLegalActions(ag)
            for i in actList:
                suc = gState.generateSuccessor(ag, i)
                sucDes = getMinMax(suc, dep, ag + 1)
                if type(sucDes) is float:
                    sucVal = sucDes
                else:
                    sucVal = sucDes[0]

                if ag != 0 and sucVal < des[0]:
                    des = [sucVal, i]
                if ag == 0 and sucVal > des[0]:
                    des = [sucVal, i]
            return des

        return getMinMax(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        

        def get(st, ag, dep, a, b):
            ag = ag % st.getNumAgents()
            if st.isWin() or st.isLose() or dep == 0:
                return self.evaluationFunction(st)
            elif ag == 0:
                return calculate(st, ag, dep, a, b, max, -10000000000)
            else:
                return calculate(st, ag, dep, a, b, min, 10000000000)

        def calculate(st, ag, dep, a, b, fun, sc):
            move = st.getLegalActions(ag)
            for i in move:
                sc = fun(sc, get(st.generateSuccessor(ag, i), ag + 1, dep - 1, a, b)) 
                if fun is max:
                    if sc > b:
                        return sc
                    a = fun(a, sc)
                elif fun is min:
                    if sc < a:
                        return sc
                    b = fun(b, sc)
            return sc


        move = gameState.getLegalActions(0)
        ans = None
        a = -10000000000
        b = 10000000000

        for i in move:
            dep = self.depth * gameState.getNumAgents()
            sc = get(gameState.generateSuccessor(0, i), 1, dep - 1, a, b)
            if sc > a:
                ans = i
                a = sc

        return ans


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        

        def getMax(gState, dep, ag):
            des = None
            if ag == gState.getNumAgents():
                ag = 0
                dep = dep + 1
            if gState.isWin() or gState.isLose() or dep == self.depth:
                return self.evaluationFunction(gState)
            if ag == 0:
                des = [-100000000000, ""]
            else:
                des = [0, ""]

            actList = gState.getLegalActions(ag)
            for i in actList:
                suc = gState.generateSuccessor(ag, i)
                sucDes = getMax(suc, dep, ag + 1)

                if type(sucDes) is float:
                    sucVal = sucDes
                else:
                    sucVal = sucDes[0]

                if ag != 0:
                    des = [sucVal / len(actList) + des[0], i]
                if ag == 0 and sucVal > des[0]:
                    des = [sucVal, i]

            return des

        return getMax(gameState, 0, 0)[1]



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    
    newPos = currentGameState.getPacmanPosition()
    newFoods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    ghostNear = 10000000000
    foodNear = 10000000000
    for i in ghostStates:
        ghostDist = manhattanDistance(newPos, i.configuration.pos)
        if i.scaredTimer == 0:
            ghostNear = min(ghostNear, ghostDist, newPos)
        else:
            ghostNear = -10

    if not newFoods.asList():
        foodNear = 0
    else:
        for i in newFoods.asList():
            foodNear = min(foodNear, manhattanDistance(i, newPos))

    good = currentGameState.getScore()
    bad = 7/(ghostNear + 1) + foodNear/3
    score = good - bad
    return score


# Abbreviation
better = betterEvaluationFunction
 