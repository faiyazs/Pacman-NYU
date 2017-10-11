

from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random
from collections import deque
class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    def registerInitialState(self, state):
        #self.visited((0,0)) = True
        return;

    def getAction(self, state):
        stack = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            #store score, action ,state
            nextstate = state.generatePacmanSuccessor(action)
            firsttScore = scoreEvaluation(nextstate)
            if nextstate.isWin():
                return action[1]
            if nextstate.isLose():
                continue
            stack.append([nextstate,action,firsttScore])
        while stack:
            #pop first action
            nextt = stack.pop(0)
            nextaction = nextt[1]
            nxtstate = nextt[0]
            legal = nxtstate.getLegalPacmanActions()
            for action in legal:
                generateSuccessor = nxtstate.generatePacmanSuccessor(action)
                if nextstate.isWin():
                    return action[1]
                if generateSuccessor is None:
                    path = max(stack,key=lambda x:x[2])[1]
                    return path

                if generateSuccessor not in stack:
                    score = scoreEvaluation(generateSuccessor)
                    successorss = generateSuccessor
                    actionss=nextaction
                    newPath = (successorss,actionss,score)
                    stack.append(newPath)

class DFSAgent(Agent):
    def registerInitialState(self, state):
        return


    def getAction(self, state):
        stack = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            #store score, action ,state
            nextstate = state.generatePacmanSuccessor(action)
            firsttScore = scoreEvaluation(nextstate)
            if nextstate.isWin():
                return action[1]
            if nextstate.isLose():
                continue
            stack.append([nextstate,action,firsttScore])
        while stack:
            #pop first action
            nextt = stack.pop()
            nextaction = nextt[1]
            st = nextt[0]
            legal = st.getLegalPacmanActions()
            for action in legal:
                generateSuccessor = st.generatePacmanSuccessor(action)
                if nextstate.isWin():
                    return action[1]
                if generateSuccessor is None:
                    path = max(stack,key=lambda x:x[2])[1]
                    return path

                if generateSuccessor not in stack:
                    score = scoreEvaluation(generateSuccessor)
                    newPath = (generateSuccessor,nextaction,score)
                    stack.append(newPath)


class AStarAgent(Agent):
    def registerInitialState(self, state):
        return;
    def getAction(self, state):
        legalActions = state.getLegalPacmanActions()
        generatenext = [(state.generatePacmanSuccessor(action), action) for action in legalActions]
        scoreRecord = []
        notvisited = []
        
        visited = False

        while(1):
            temporary = []
            for child in generatenext:
                nextstate = child[0]

                if nextstate.isWin():
                    return child[1]
                if nextstate.isLose():
                    continue

                #print child[1]
                legal = nextstate.getLegalPacmanActions()
                #print legal
                for c in legal:
                    nextt = nextstate.generatePacmanSuccessor(c)
                    #print nextt
                    if nextt is None:
                        visited = True
                        break

                    else:
                        temporary.append((nextt,child[1],1))
            if visited == True:
                break
            else: 
                notvisited.extend(temporary)
                a = notvisited.pop(0)
                notvisited.sort(key=lambda x: scoreEvaluation(x[0])+x[2])
                if child[0].isWin():
                    return child[1]
                if child[0].isLose():
                    #print(c)
                    continue
        for child in notvisited:
            scored = (scoreEvaluation(child[0]))
            action = child[1]
            scoreRecord.append((scored,action))
        bestScore = max(scoreRecord)[0]
        bestActions = [pair[1] for pair in scoreRecord if pair[0] == bestScore]
        return random.choice(bestActions)

