import requests
from queries import *
# print('set query' + setQuery)
header = {"Authorization" : "Bearer 8a4affeca417cac84a209ebf37e8a8d6"}   
url = 'https://api.start.gg/gql/alpha'
# list of tournaments to use
tournaments = []
# eventID list via comprehension
eventIDs = [getEventID(tourney) for tourney in tournaments]
for ID in eventIDs:
    totalPages = getTotalPagesSet(ID)
    for page in range(1, totalPages + 1):
        sets = 