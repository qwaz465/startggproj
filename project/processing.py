# from the_project import *
from queries import *
import numpy as np
import math
# for 1 tournament, grab all sets by page and adds IDs to setList and returns it
# DO NOT USE THE WORD SET IT FUCKS EVERYTHING UP!!!!!!
def getSetIDs(eventID):
    setList = []
    # getting page count for bracket
    totalPages = getTotalPagesSet(eventID)
    for page in range(1, totalPages + 1):
        # getting all set maps on a page
        sets = getSetsOnePage(eventID, page)
        # getting actual set IDs
        for setMap in sets:
            smashSet = setMap['id']
            setList.append(smashSet)
    return setList

# take list of all sets and extract players to put in a set to store all players in given tournaments, size is recorded to make matrix
# def playerList(sets):
#     players = set()
#     # print(type(players))
#     # print(players)
#     for smashSet in sets:
#         # print(smashSet)
#         names = list(smashSet.keys())
#         # print(names)
#         p1name = names[0]
#         p2name = names[1]
#         players.add(p1name)
#         players.add(p2name)
#     return players

def playerList(sets):
    players = set()
    for smashSet in sets:
        # Ensure smashSet has at least two keys
        if len(smashSet) < 2:
            print(f"Warning: Unexpected smashSet format: {smashSet}")
            continue  # Skip this iteration
        
        names = list(smashSet.keys())
        p1name = names[0]
        p2name = names[1]
        players.add(p1name)
        players.add(p2name)
    return players

# makes set matrix where set count will go into, value in (0,2) is sets player 0 has on player 2, value in (2,0) is opposite
# also makes similar game matrix
# also makes dictionary to map player name to index in matrices
def makeMatrices(players, sets):
    playerCount = len(players)
    # set up empty matrices
    setMatrix = np.zeros((playerCount, playerCount))
    gameMatrix = np.zeros((playerCount, playerCount))
    # set up empty dict
    playerMatrixIndex = {}
    ind = 0
    # assigns player to index in matrices
    for player in players:
        playerMatrixIndex[player] = ind
        ind += 1
    for smashSet in sets:
        names = list(smashSet.keys())
        p1name = names[0]
        p2name = names[1]
        scores = list(smashSet.values())
        p1score = scores[0]
        p2score = scores[1]
        p1index = playerMatrixIndex[p1name]
        p2index = playerMatrixIndex[p2name]
        # dq case
        if p1score is None or p2score is None:
            break
        # updating game mat
        gameMatrix[p1index, p2index] += p1score
        gameMatrix[p2index, p1index] += p2score
        # p1 won set case
        if p1score > p2score:
            setMatrix[p1index, p2index] += 1
        # p2 won set case
        else:
            setMatrix[p2index, p1index] += 1
    return playerMatrixIndex, gameMatrix, setMatrix

# # updateElo takes elo map and a set and computes updated elo score and returns the new updated elo map
# def updateElo(elo, smashSet):
#     print(smashSet)
#     print(elo)
#     names = list(smashSet.keys())
#     print(names)
#     p1name = names[0]
#     p2name = names[1]
#     scores = list(smashSet.values())
#     print(scores)
#     p1score = scores[0]
#     p2score = scores[1]
#     # stop here if dq set
#     if p1score is None or p2score is None:
#         return elo
#     p1rank = elo[p1name]
#     p2rank = elo[p2name]
#     # elo probability
#     p1prob = 1.0/(1 + math.pow(10, (p1rank - p2rank) / 400.0))
#     p2prob = 1.0 - p1prob
#     # 1 is p1 win, 0 otherwise
#     if p1score > p2score:
#         outcome = 1
#     else:
#         outcome = 0
#     # k is some scaling constant, play with it later
#     k = 30
#     # updating elo
#     p1rank += k*(outcome - p1prob)
#     p2rank += k*((1 - outcome) - p2prob)
#     print(p1rank)
#     print(p2rank)
#     # updating elo map
#     elo[p1name] = p1rank
#     elo[p2name] = p2rank
#     return elo


def updateElo(elo, smashSet):
    print(smashSet)
    print(elo)
    
    # Get the player names
    names = list(smashSet.keys())
    print(names)
    
    # Check if the smashSet has at least two players
    if len(names) < 2:
        print(f"Warning: Incomplete smashSet: {smashSet}")
        return elo  # Skip this set
    
    p1name = names[0]
    p2name = names[1]
    
    # Get the scores
    scores = list(smashSet.values())
    print(scores)
    
    p1score = scores[0]
    p2score = scores[1]
    
    # Stop here if the set contains disqualifications or invalid scores
    if p1score is None or p2score is None:
        print(f"Disqualified set: {smashSet}")
        return elo
    
    p1rank = elo.get(p1name, 1500)  # Default to 1500 if player not in elo map
    p2rank = elo.get(p2name, 1500)  # Default to 1500 if player not in elo map
    
    # Elo probability
    p1prob = 1.0 / (1 + math.pow(10, (p2rank - p1rank) / 400.0))
    p2prob = 1.0 - p1prob
    
    # Determine the outcome
    outcome = 1 if p1score > p2score else 0
    
    # K is a scaling constant
    k = 30
    
    # Update ranks
    p1rank += k * (outcome - p1prob)
    p2rank += k * ((1 - outcome) - p2prob)
    
    print(p1rank)
    print(p2rank)
    
    # Update the elo map
    elo[p1name] = p1rank
    elo[p2name] = p2rank
    
    return elo

# sorts elo map by value and stays as dictionary
def sortElo(elo):
    eloSorted = sorted(elo.items(), key = lambda x: x[1], reverse = True)
    eloSorted = dict(eloSorted)
    return eloSorted