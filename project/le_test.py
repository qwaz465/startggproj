import requests
from queries import *
from processing import *
header = {"Authorization" : "Bearer 8a4affeca417cac84a209ebf37e8a8d6"}   
url = 'https://api.start.gg/gql/alpha'
query = '''
query Lawls($slug: String) {
  user(slug: $slug) {
    id
    bio
    name
    location {
        city
    }
    player {
      id
      gamerTag
    }
  }
}
'''
# setQuery stuff
variables = {"eventId" : "1127053", "page" : 1, "perPage" : 10}
json_request = {"query" : setQuery, "variables" : variables}
request = requests.post(url = url, json = json_request, headers = header)
response = request.json()
# store this number to iterate through requests
print(response['data']['event']['sets']['pageInfo']['totalPages'])
# this grabs all set ids in a list where each entry is a map with 'id' as the key
print(response['data']['event']['sets']['nodes'])

# a big test
id = getEventID('tournament/finals-destination-14/event/ultimate-singles')
print(id)
a_set = getSetsOnePage(id, 1)[1]['id']
print(a_set)
getPlayersAndScore(a_set)

# getSetsOnePage checks
id = getEventID('tournament/finals-destination-14/event/ultimate-singles')
print(id)
sets = getSetsOnePage(id, 1)
print(sets)

# getSetIDs testinbgf
id = getEventID('tournament/finals-destination-14/event/ultimate-singles')
getSetIDs(id)


# large flow test (will continue to update as new stuff is implemented)
# list of tournaments to use
tournaments = ['tournament/finals-destination-14/event/ultimate-singles', 'tournament/smash-at-the-made-45/event/smash-ultimate-singles']
# eventID list via comprehension
eventIDs = [getEventID(tourney) for tourney in tournaments]
print(eventIDs)
setIDs = []
# get all set IDs using function in processing, test next time you read this
for ID in eventIDs:
  setIDTemp = getSetIDs(ID)
  setIDs.extend(setIDTemp)
print(setIDs)
# use set ids to get actual set counts as a list of maps where each map represents a set {p1 : score, p2 : score}
sets = []
for setID in setIDs:
  smashSet = getPlayersAndScore(setID)
  sets.append(smashSet)
print(sets)
players = playerList(sets)
print(players)
print(len(players))
print(playerList(sets))
# test above flow next time, also think of how to extract and put in matrix/process players