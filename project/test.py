import requests
from queries import *
from processing import *
from keys import api_key
import numpy as np
header = {"Authorization" : api_key}   
url = 'https://api.start.gg/gql/alpha'

#
# list of tournaments to use
tournaments = ['tournament/finals-destination-14/event/ultimate-singles', 'tournament/finals-destination-15/event/ultimate-singles']
# eventID list via comprehension
eventIDs = [getEventID(tourney) for tourney in tournaments]
print(eventIDs)
setIDs = []
# get all set IDs
for ID in eventIDs:
  setIDTemp = getSetIDs(ID)
  setIDs.extend(setIDTemp)
print(setIDs)
print(len(setIDs))
# use set ids to get actual set counts as a list of maps where each map represents a set {p1 : score, p2 : score}
sets = []
x = 0
for setID in setIDs:
  print(x)
  x += 1
  # print(setID)
  smashSet = getPlayersAndScore(setID)
  # print(smashSet)
  sets.append(smashSet)
print(sets)
print(len(sets))
players = playerList(sets)
print(players)
print(len(players))
playerCount = len(players)

playerMatrixIndex, gameMatrix, setMatrix = makeMatrices(players, sets)
print(playerMatrixIndex)
print(gameMatrix)
print(setMatrix)
# retrieving shaveh uzo set/game count, should be 1-0/3-0 respectively
print(setMatrix[26, 36])
print(setMatrix[36, 26])
print(gameMatrix[26, 36])
print(gameMatrix[36, 26])
elo = {player:1500 for player in players}
print(elo)
for smashSet in sets:
  elo = updateElo(elo, smashSet)
elo = sortElo(elo)
print(elo)
