import requests
header = {"Authorization" : "Bearer 8a4affeca417cac84a209ebf37e8a8d6"}   
url = 'https://api.start.gg/gql/alpha'

eventIDQuery = '''
query getEventId($slug: String) {
  event(slug: $slug) {
    id
    name
  }
},
'''
# returns event id lawls
def getEventID(slug):
    variables = {"slug" : slug}
    json_request = {"query" : eventIDQuery, "variables" : variables}
    request = requests.post(url = url, json = json_request, headers = header)
    response = request.json()
    print(response['data']['event']['name'])
    return response['data']['event']['id']
setQuery = '''
query EventSets($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(page: $page, perPage: $perPage, sortType: STANDARD) {
      pageInfo {
        total
        totalPages
      }
      nodes {
        id
      }
    }
  }
},
'''
# returns amount of pages, use this to iterate through next func
def getTotalPagesSet(eventId):
    variables = {"eventId" : eventId, "page" : 1, "perPage" : 40}
    json_request = {"query" : setQuery, "variables" : variables}
    request = requests.post(url = url, json = json_request, headers = header)
    response = request.json()
    return response['data']['event']['sets']['pageInfo']['totalPages']
# returns list of 'id' : actual id maps, iterate through this later to grab set IDs
def getSetsOnePage(eventId, page):
    variables = {"eventId" : eventId, "page" : page, "perPage" : 40}
    json_request = {"query" : setQuery, "variables" : variables}
    request = requests.post(url = url, json = json_request, headers = header)
    response = request.json()
    return response['data']['event']['sets']['nodes']

setQueryBackUp = '''
query EventSets($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      pageInfo {
        total
        totalPages
      }
      nodes {
        id
        slots {
          id
          entrant {
            id
            name
          }
        }
      }
    }
  }
},
'''
playerAndScoreQuery = '''
query SetsAndPlayers($setId: ID!) {
  set(id: $setId) {
    state
    slots {
      entrant {
        participants {
          player {
            gamerTag
            prefix
          }
        }
      }
      standing {
        stats {
          score {
            value
          }
        }
      }
    }
  }
}
'''
def getPlayersAndScore(setId):
    variables = {"setId" : setId}
    json_request = {"query" : playerAndScoreQuery, "variables" : variables}
    request = requests.post(url = url, json = json_request, headers = header)
    response = request.json()
    # print(response)
    # list of len 2, each is map of stuff to right of query, extract accordingly
    # split list into 2 maps, grab vals
    stuff = response['data']['set']['slots']
    print(stuff)
    p1Name = stuff[0]['entrant']['participants'][0]['player']['gamerTag']
    p1Pre = stuff[0]['entrant']['participants'][0]['player']['prefix']
    p1Score = stuff[0]['standing']['stats']['score']['value']
    p2Name = stuff[1]['entrant']['participants'][0]['player']['gamerTag']
    p2Pre = stuff[1]['entrant']['participants'][0]['player']['prefix']
    p2Score = stuff[1]['standing']['stats']['score']['value']
    if p1Pre == None:
        p1Pre = ''
    if p2Pre == None:
        p2Pre = ''
    print(p1Pre + ' ' + p1Name + ':' + str(p1Score))
    print(p2Pre + ' ' + p2Name + ':' + str(p2Score))
    p1NameFull = p1Pre + ' ' + p1Name
    p2NameFull = p2Pre + ' ' + p2Name