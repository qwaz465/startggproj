import requests
from queries import *
from processing import *
# print('set query' + setQuery)
header = {"Authorization" : "Bearer 8a4affeca417cac84a209ebf37e8a8d6"}   
url = 'https://api.start.gg/gql/alpha'
# list of tournaments to use
tournaments = []
# eventID list via comprehension
eventIDs = [getEventID(tourney) for tourney in tournaments]
setIDs = []
# get all set IDs using function in processing, test next time you read this
for ID in eventIDs:
    setIDTemp = getSetIDs(ID)
    setIDs.extend(setIDTemp)
# use set ids to get actual set counts as a list of maps where each map represents a set {p1 : score, p2 : score}
sets = []
for setID in setIDs:
    smashSet = getPlayersAndScore(setID)
    sets.append(smashSet)
# test above flow next time, also think of how to extract and put in matrix/process players
# above is tested, but need to think how to extract/make matrix
# make set of players and store size of set to make ssbu set score matrix
players = playerList(sets)
playerCount = len(players)