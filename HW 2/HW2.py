# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 14:30:41 2017

@author: SHILPASHREE RAO
"""
import sys
with open(sys.argv[2]) as file:
    from collections import OrderedDict


###############################################################################
#GLOBAL INITIALIZATIONS
    pinf = float("inf")    
    ninf = float("-inf")
    ###############################################################################
    
    #file = open("t10.txt","r") 
    lines = file.read().splitlines()
    file.close()
    colours = lines[0].split(', ')
    colours = [x.strip(' ') for x in colours]  ##added new
    ini_assign = lines[1]
    treeDepth = int(lines[2].strip(' '))
    P1_pref = lines[3]
    P2_pref = lines[4]
    graphlines = lines[5: ]
    
    ####creating dictionary for initial assigned map#######
    curr = ini_assign.split(', ')
    node_list = []
    ini_colr = []
    ini_plyr = []
    for nodes in range(len(curr)):
        curr_node = curr[nodes].split(': ')[0]
        node_list.append(curr_node)
        curr_colr = curr[nodes].split(': ')[1].split('-')[0]
        ini_colr.append(curr_colr)
        curr_plyr = curr[nodes].split(': ')[1].split('-')[1]
        ini_plyr.append(curr_plyr)
    node_list = [x.strip(' ') for x in node_list]              ##added new
    ini_plyr = [x.strip(' ') for x in ini_plyr]                ##added new
    dict_iniassignc = OrderedDict(zip(node_list, ini_colr))    #arranaged in inserted order(access keys this way, for root node)dict_iniassignc.keys()[-1]
    dict_iniassignp = OrderedDict(zip(node_list, ini_plyr))    #arranaged in inserted order
        
    ####creating dictionary for colour preference/scores of player 1#######
    pref_col1 = []
    pref_ord1 = []
    pref_list1 = P1_pref.split(', ')
    for col in range(len(pref_list1)):
        curr_col = pref_list1[col].split(': ')[0]
        pref_col1.append(curr_col)
        curr_ord = int(pref_list1[col].split(': ')[1])
        pref_ord1.append(curr_ord)
    pref_col1 = [x.strip(' ') for x in pref_col1]
    dict_prefP1 = OrderedDict(zip(pref_col1, pref_ord1))
    
    ####creating dictionary for colour preference of player 2#######
    pref_clr2 = []
    pref_ord2 = []
    pref_list2 = P2_pref.split(', ')
    for clr in range(len(pref_list2)):
        cur_clr = pref_list2[clr].split(': ')[0]
        pref_clr2.append(cur_clr)
        cur_ord = int(pref_list2[clr].split(': ')[1])
        pref_ord2.append(cur_ord)
    pref_clr2 = [x.strip(' ') for x in pref_clr2]
    dict_prefP2 = OrderedDict(zip(pref_clr2, pref_ord2))
    
    ####creating dictionary for the graph#######
    par_node = []
    chi_node = []
    child_nodelist = []
    for line in range(len(graphlines)):
        eachline = graphlines[line].split(': ')
        par_node.append(eachline[0])
        cur_chi_node = eachline[1]
        sub_cur_node = sorted(cur_chi_node.split(', '))
        chi_node.append(sub_cur_node)
    par_node = [x.strip(' ') for x in par_node]
    dict_graph = dict(zip(par_node, chi_node)) #print dict_graph.items()[0][0] = 1st parent node, print dict_graph.items()[0][1] = nodes connected to it displyed as a list
    #print sorted(dict_graph.keys())

def calculateCouldBeColored(alreadyColored):
    a = []
    for i in alreadyColored:
        for j in dict_graph[i]:
            if j.strip() not in alreadyColored:
                a.append(j.strip())
    return a
      
def remColrs(canbclrd, alrdyclrd):
    clrslst = []
    for i in canbclrd: 
        neighbrs = [x.strip() for x in dict_graph[i]]  
        nodeclr = [alrdyclrd[j] for j in neighbrs if j in alrdyclrd] 
        colrspernode = sorted([c for c in colours if c not in nodeclr])
        clrslst.append(colrspernode)
    return clrslst

def calculateFrontier(couldBeColoredList, remainingColors):
    frontierList = []
    for i in range(len(couldBeColoredList)):
        if(remainingColors[i]!=[]):
            for j in remainingColors[i]:
                frontierList.append([couldBeColoredList[i], j]) 
        else:
            frontierList.append([couldBeColoredList[i], ''])
    return frontierList

def terminationCondition(depth, couldBeColored, nodeColor):
    if((depth == treeDepth) or (couldBeColored == []) or (nodeColor == '')):
        return True
    else: 
        return False
    
def calculateScores(depth, scoreP1, scoreP2, poppedChild):
    if(depth%2 == 0):
        if(poppedChild[1] == ''):
            scoreP2.append(0)
        else:
            scoreP2.append(int(dict_prefP2[poppedChild[1]]))
    else:
        if(poppedChild[1] == ''):
            scoreP1.append(0)
        else:
            scoreP1.append(int(dict_prefP1[poppedChild[1]]))
    return scoreP1, scoreP2
    
def Eval_func (scoreP1, scoreP2):   
    totalScoreP1 = sum(int(i) for i in scoreP1)
    totalScoreP2 = sum(int(i) for i in scoreP2)
    evalFuncn = totalScoreP1 - totalScoreP2
    return evalFuncn

def initializeValues(alpha, beta, depth, values, poppedChild):
    if(depth%2 == 0):
        #values[(poppedChild[0],poppedChild[1])] = [ninf, alpha, beta, depth]  
        values[depth] = [ninf, alpha, beta]
    else:
        #values[(poppedChild[0],poppedChild[1])] = [pinf, alpha, beta, depth]
        values[depth] = [pinf, alpha, beta]
    return values

def findNewV(newV, oldV, depth):
    if(depth%2 == 0):
        return max(newV, oldV)
    else:    
        return min(newV, oldV)
    
def removeScore(scoreP1, scoreP2, depth):
    if(depth%2 == 0):
        del scoreP2[-1]
        return scoreP1, scoreP2
    else:
        del scoreP1[-1]
        return scoreP1, scoreP2
    
def updateAlphaBeta(alp, bet, v, depth):
    if((v >= alp) and (v<=bet)):
        if(depth%2==0):
            alp = v
        else:
            bet = v
    return alp, bet
    
###############################################################################

output = ''
root = dict_iniassignc.keys()[-1]
alreadyColored = OrderedDict(zip(dict_iniassignc.keys(), \
                                 dict_iniassignc.values()))

values = {0: [ninf, ninf, pinf]}
depth = 0
v = values[0][0]
alpha = values[0][1]
beta = values[0][2]
output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
    + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
score1, score2 = [], []
for i in dict_iniassignc:
    if dict_iniassignp[i] is '1':
        score1.append(int(dict_prefP1[dict_iniassignc[i]]))
    else:
        score2.append(int(dict_prefP2[dict_iniassignc[i]]))
frontier = {i: [] for i in range(int(treeDepth)+1)}

dictMapping = {0: ['', '']}
couldBeColored = dict()
backTrack = False
done = False
bestMove = dict()

while(done == False): 
    couldBeColored[depth] = \
                      sorted(set(calculateCouldBeColored(alreadyColored)))
    if(backTrack == False):
        remainingColors = remColrs(couldBeColored[depth], \
                                   alreadyColored)
        frontier[depth] = calculateFrontier(couldBeColored[depth], \
                                             remainingColors)
        randomflag = True
        
    count = 0
    if(len(frontier[depth]) != 0 and depth!=treeDepth):
        randomflag = False
        for i in frontier[depth]:
            if(i[1]==''):
                count = count + 1
        if(count == len(frontier[depth])):
            evalValue = Eval_func(score1, score2)
            v = findNewV(evalValue, values[depth][0], depth)
            values[depth][0] = v
            alpha = values[depth][1]
            beta = values[depth][2]
            output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
                    + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
            currNode = [alreadyColored.keys()[-1], alreadyColored.values()[-1]]
            del alreadyColored[currNode[0]]
            depth = depth - 1
            backTrack = True   
            v = findNewV(values[depth+1][0], values[depth][0], depth)
            values[depth][0] = v

            output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
                    + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
            continue

    if(depth == 1):
        bestMove[(alreadyColored.keys()[-1], alreadyColored.values()[-1])] = v
    
    backTrack = False    
    condition1 = ((depth%2==0) and (v>=beta)) or ((depth%2==1) and (v<=alpha))
    condition2 = terminationCondition(depth, couldBeColored, \
                                alreadyColored.values()[-1])
    condition3 = (frontier[depth] == [])
    
    if((condition1 == False) and (condition2 == False) and (condition3 == False)):                    
        popChild = frontier[depth].pop(0)
        alreadyColored[popChild[0]] = popChild[1]
        depth = depth + 1
        score1, score2 = calculateScores(depth, score1, score2, popChild)
        values = initializeValues(alpha, beta, depth, values, popChild) 
        v = values[depth][0]
        alpha = values[depth][1]
        beta = values[depth][2]
        if(terminationCondition(depth, sorted(set(calculateCouldBeColored(alreadyColored))), \
                                alreadyColored.values()[-1]) == False):
            ##########
            a = sorted(set(calculateCouldBeColored(alreadyColored)))
            b = remColrs(a, alreadyColored)
            c = calculateFrontier(a, b)
            count1 = 0
            if(len(c) != 0 and depth!=treeDepth):
                
                for i in c:
                    if(i[1]==''):
                        count1 = count1 + 1
                if(count1 != len(c)):
            ##########
                    output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
                    + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
    else:
        flagNoColor = False
        if condition2:
            evalValue = Eval_func(score1, score2)
            v = findNewV(evalValue, values[depth][0], depth)
            values[depth][0] = v
            if(alreadyColored.values()[-1] != ''):  
                output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
                + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
            else:
                flagNoColor = True
            condition2 = False
        if(depth == 0):
            break
        currNode = [alreadyColored.keys()[-1], alreadyColored.values()[-1]]
        del alreadyColored[currNode[0]]
        score1, score2 = removeScore(score1, score2, depth)
        depth = depth - 1
        backTrack = True
        vold = values[depth][0]
        alphaold = values[depth][1]
        betaold = values[depth][2]

        v = findNewV(values[depth+1][0], values[depth][0], depth)
        alpha, beta = updateAlphaBeta(values[depth][1], values[depth][2], \
                                          v, depth)
        if((flagNoColor == True) and (((depth%2==0 and v>=betaold) or (depth%2==1 and v<=alphaold)) == True)):
            v = vold
            alpha = alphaold
            beta = betaold
        elif(flagNoColor == True):
            v = vold
            alpha = alphaold
            beta = betaold
        elif((((depth%2==0 and v>=betaold) or (depth%2==1 and v<=alphaold)) == True)):
            alpha = alphaold
            beta = betaold
        
        values[depth][0] = v
        values[depth][1] = alpha
        values[depth][2] = beta
        
        if(flagNoColor == False):
            output += alreadyColored.keys()[-1] + ', ' + alreadyColored.values()[-1] \
                + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n'
           
some = [bestMove[i] for i in bestMove.keys()]                
maxV = max(some) 
listOfKeys = sorted([i for i in bestMove.keys()])
for i in listOfKeys:
    if(bestMove[i] == maxV):
        output += i[0] + ', ' + i[1] + ', ' + str(maxV)
        break
out = open("output.txt", "wb")
out.write(output)
out.close()           
            
            
            
            
            
            
            






