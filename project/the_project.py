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