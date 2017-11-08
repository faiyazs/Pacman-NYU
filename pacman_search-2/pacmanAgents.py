

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
class HillClimberAgent(Agent):
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;
    def action(action):
        action= list()
        for action in range(1,5):
            action.append(state.getallpossibleActions())
        return action
    def getAction(self, state):
        size =False
        seq = list()
        for i in range(5): #get all possible action
            seq.append(random.choice(state.getAllPossibleActions()))
        best = [scoreEvaluation(state), [Directions.STOP]] #store best score so far
        while not size:
            nextnb = list()
            for i in range(len(seq)):
                if random.randint(1, 2) == 1: #getaction sequence 50% probability
                    nextnb.append(random.choice(state.getAllPossibleActions()))
                else:
                    nextnb.append(seq[i])
            current = state
            for action in nextnb:  #get neighbouring sequence
                nex= current.generatePacmanSuccessor(action)
                temp=nex

                if temp is not None and (temp.isWin() + temp.isLose()) == 0: #evaluate score
                    current = temp
                    continue
                else:
                    if temp is None:
                        size = True
            nextscore= scoreEvaluation(current)
            if  (size): #return best action
                return random.choice(best[1])
            if nextscore > best[0]: #update best score and action after comparision
                best[0] = nextscore
                best[1] = list()
            elif nextscore < best[0]:
                continue

            best[1].append(nextnb[0])
            seq = nextnb
        get = action()

class GeneticAgent(Agent):
    def registerInitialState(self, state):
        return;
    def getAction(self, state):

        sumRank = 36 #rank selection
        rankpopulation = list()
        for i in range(8):
            rankpopulation.append(8-i)
        winAction = None
        score = [-78766.89, []]
        population = list()
        for i in range(8): #generate the population / initialize
            sequence = list()
            for j in range(5):
                sequence.append(random.choice(state.getAllPossibleActions()))
            population.append([sequence, 0])
        breakLoop = False
        while True:
            for mytuple in population: #score each  poulation and save the score
                current = state
                for i in range(0,5):
                    current = current.generatePacmanSuccessor(mytuple[0][i])
                    if current is None:
                        breakLoop = True
                        break
                    if current.isWin():
                        return mytuple[0][i]
                    if current.isLose():
                        break
                if breakLoop:
                    break
                mytuple[1] = scoreEvaluation(current)
            if breakLoop:
                break
            population.sort(key=lambda x: x[1]) #sorting population according to scores

            maxScore = population[len(population) -1][1] #fitness function , sort the chromosomes
            if maxScore > score[0]:
                score[0] = maxScore
                score[1] = list()
                for action in [mytuple[0][0] for mytuple in population if mytuple[1] == maxScore]:
                    score[1].append(action)
            for i in range(8): #sort the population according to rank
                size,index = 0,-1

                while size < random.randint(1, sumRank):
                    index += 1
                    size += rankpopulation[index]
                population.append(population[index])
            for i in range(8):
                population.pop(0)
            for i in range(4):
                if random.randint(1,10)<=7 : #reproduction ,combine parents #70% probability
                    child1 = [[], 0]
                    child2 = [[], 0]
                    parent1 = population[i*2]
                    parent2 = population[i*2+1]
                    for j in range(5):
                        if random.randint(1,2)==1:
                            child1[0].append(parent1[0][j])
                        else:
                            child1[0].append(parent2[0][j])
                        if random.randint(1,2)==1:
                            child2[0].append(parent1[0][j])
                        else:
                            child2[0].append(parent2[0][j])
                    population[i*2] = child1
                    population[i*2+1] = child2
            for mytuple in population: #mutate
                if random.randint(1,2)==1:
                    mytuple[0][random.randint(0, len(mytuple[0])-1)] = random.choice(state.getAllPossibleActions())
            for mytuple in population:
                mytuple[1] = -7878.0078
        population.sort(key=lambda x: x[1]) #best score
        maxScore = population[0][1]
        if maxScore < score[0]:
            optimal = score[1]
        else:
            optimal =[mytuple[0][0] for mytuple in population if mytuple[1] == maxScore]
        return random.choice(optimal)


class MCTSAgent(Agent):

    def registerInitialState(self, state):
        return

    def getAction(self, state):


        main = state

        def calculateUCT(node, pVisits): #UCT score
            return node[4] / float(node[1]) + (math.sqrt(2 * math.log(float(pVisits)) / float(node[1])))

        def generate(node):#expand tree #node[0] =action node[1]=visit node[2]=parent node[3]=children nodes node[4] =score
            curNode = node
            curState = curNode[0]
            result = -1
            while True:
                expanded = True #check fully expanded or not and backpropagate
                if not curNode[3]:
                    expanded = False
                for child in curNode[3]:
                    if child[1] == 0:
                        expanded = False
                if not expanded:
                    break
                curNode[3].sort(key=lambda x: calculateUCT(x, curNode[1]))
                curNode = curNode[3][len(curNode[3]) - 1]
                curState = curState.generatePacmanSuccessor(curNode[0])
                if curState is None:
                    result = None
                    break
                if curState.isWin() or curState.isLose(): #calculate score , if win or lose
                    reward = normalizedScoreEvaluation(main, curState)
                    tempNode = curNode
                    while tempNode is not None:
                        tempNode[4] += reward
                        tempNode[1] += 1
                        tempNode = tempNode[2]
                    result = next
                    break
            if result != -1:
                return result
            state = curState
            node = curNode
            if not node[3]:
                legal = state.getLegalPacmanActions()
                for action in legal:
                    node[3].append([action, 0, node, [], 0])
                nodeToReturn = node[3][0]
                curState = state.generatePacmanSuccessor(node[3][0][0])
                if curState is None:
                    return None
                if curState.isWin or curState.isLose:
                    reward = normalizedScoreEvaluation(main, curState)
                    tempNode = nodeToReturn
                    while tempNode is not None:
                        tempNode[4] += reward
                        tempNode[1] += 1
                        tempNode = tempNode[2]
                    return next
                return [nodeToReturn, curState]
            nodeToReturn = None
            for child in node[3]:
                if child[1] == 0:
                    nodeToReturn = child
                    curState = state.generatePacmanSuccessor(child[0])
                    if curState is None:
                        return None
                    if curState.isWin or curState.isLose:
                        reward = normalizedScoreEvaluation(main, curState)
                        tempNode = child
                        while tempNode is not None: #backpropagate
                            tempNode[4] += reward
                            tempNode[1] += 1
                            tempNode = tempNode[2]
                        return next
                    legal = curState.getLegalPacmanActions()
                    for action in legal:
                        child[3].append([action, 0, child, [], 0])
                    break
            return [nodeToReturn, curState]


        rootNode = [main,  0,  None,  [], 0]
        legal = rootNode[0].getLegalPacmanActions()
        for action in legal:
            rootNode[3].append([action, 0, rootNode, [], 0])
        while True:
            result = generate(rootNode)
            if result is None:
                break
            elif result == next:
                continue
            curState = result[1]
            for i in range(0,5): #Default Tree #check for succsors and win and lose states and return the children #rollout
                legal = curState.getLegalPacmanActions()
                if not curState.getLegalPacmanActions():
                    break
                temp = curState.generatePacmanSuccessor(legal[random.randint(0, len(curState.getLegalPacmanActions()) - 1)])
                if temp is None:

                    limitIsNotReached = False
                    break
                elif temp.isWin() or temp.isLose():
                    curState = temp
                    break
                curState = temp
            reward = normalizedScoreEvaluation(main, curState)
            tempNode = result[0]
            while tempNode is not None: #backpropagate
                tempNode[4] += reward
                tempNode[1] += 1
                tempNode = tempNode[2]

        mostVisitCount = max(rootNode[3], key=lambda x: x[1])[1]
        bestActions = [child[0] for child in rootNode[3] if child[1] == mostVisitCount]
        return random.choice(bestActions)
