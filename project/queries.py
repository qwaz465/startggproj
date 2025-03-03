import requests
from limiter import Limiter
from keys import api_key
header = {"Authorization" : api_key}   
url = 'https://api.start.gg/gql/alpha'
rate_limiter = Limiter(rate=1.1, capacity=1)

eventIDQuery = '''
query getEventId($slug: String) {
  event(slug: $slug) {
    id
    name
  }
},
'''
# returns event id lawls
@rate_limiter
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
@rate_limiter
def getTotalPagesSet(eventId):
    variables = {"eventId" : eventId, "page" : 1, "perPage" : 40}
    json_request = {"query" : setQuery, "variables" : variables}
    request = requests.post(url = url, json = json_request, headers = header)
    response = request.json()
    return response['data']['event']['sets']['pageInfo']['totalPages']

# returns list of 'id' : actual id maps, iterate through this later to grab set IDs
@rate_limiter
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
# @rate_limiter
# def getPlayersAndScore(setId):
#     variables = {"setId" : setId}
#     json_request = {"query" : playerAndScoreQuery, "variables" : variables}
#     request = requests.post(url = url, json = json_request, headers = header)
#     response = request.json()
#     # print(response)
#     # list of len 2, each is map of stuff to right of query, extract accordingly
#     # split list into 2 maps, grab vals
#     print(response)
#     stuff = response['data']['set']['slots']
#     # print(stuff)
#     p1Name = stuff[0]['entrant']['participants'][0]['player']['gamerTag']
#     p1Pre = stuff[0]['entrant']['participants'][0]['player']['prefix']
#     p1Score = stuff[0]['standing']['stats']['score']['value']
#     p2Name = stuff[1]['entrant']['participants'][0]['player']['gamerTag']
#     p2Pre = stuff[1]['entrant']['participants'][0]['player']['prefix']
#     p2Score = stuff[1]['standing']['stats']['score']['value']
#     if p1Pre == None:
#         p1Pre = ''
#     if p2Pre == None:
#         p2Pre = ''
#     # print(p1Pre + ' ' + p1Name + ':' + str(p1Score))
#     # print(p2Pre + ' ' + p2Name + ':' + str(p2Score))
#     if p1Pre == '':
#       p1NameFull = p1Name
#     else:
#       p1NameFull = p1Pre + ' | ' + p1Name
#     if p2Pre == '':
#       p2NameFull = p2Name
#     else:
#       p2NameFull = p2Pre + ' | ' + p2Name
#     return {p1NameFull : p1Score, p2NameFull : p2Score}

@rate_limiter
def getPlayersAndScore(setId, cache):
    # Check if result is cached
    if setId in cache:
        print(f"Cache hit for setId: {setId}")
        return cache[setId]

    variables = {"setId": setId}
    json_request = {"query": playerAndScoreQuery, "variables": variables}

    # Debugging: Print request payload
    print(f"Request payload for setId {setId}: {json_request}")

    try:
        request = requests.post(url=url, json=json_request, headers=header)

        # Debugging: Log status code
        print(f"Status code for setId {setId}: {request.status_code}")
        
        if request.status_code != 200:
            print(f"Error: Received non-200 status code for setId {setId}")
            print("Response text:", request.text)
            return {"Error": f"Request failed for setId {setId}"}

        # Attempt to parse JSON
        try:
            response = request.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for setId {setId}")
            print("Raw response:", request.text)
            return {"Error": f"Invalid JSON response for setId {setId}"}

        # Debugging: Print response
        print(f"Response for setId {setId}: {response}")

        # Extract data
        stuff = response.get('data', {}).get('set', {}).get('slots', None)

        if not stuff or len(stuff) < 2 or any(slot.get('entrant') is None for slot in stuff):
            print(f"Missing or incomplete data for setId: {setId}, skipping")
            return {"Error": f"Incomplete data for setId {setId}"}

        # Extract player details
        try:
            p1Name = stuff[0]['entrant']['participants'][0]['player']['gamerTag']
            p1Pre = stuff[0]['entrant']['participants'][0]['player']['prefix']
            p1Score = stuff[0]['standing']['stats']['score']['value']

            p2Name = stuff[1]['entrant']['participants'][0]['player']['gamerTag']
            p2Pre = stuff[1]['entrant']['participants'][0]['player']['prefix']
            p2Score = stuff[1]['standing']['stats']['score']['value']

            p1Pre = '' if p1Pre is None else p1Pre
            p2Pre = '' if p2Pre is None else p2Pre

            p1NameFull = p1Name if p1Pre == '' else f"{p1Pre} | {p1Name}"
            p2NameFull = p2Name if p2Pre == '' else f"{p2Pre} | {p2Name}"

            result = {p1NameFull: p1Score, p2NameFull: p2Score}

            # Cache result
            cache[setId] = result
            return result
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error extracting data for setId {setId}: {e}")
            return {"Error": f"Data extraction failed for setId {setId}"}

    except requests.RequestException as e:
        print(f"Network error for setId {setId}: {e}")
        return {"Error": f"Network error for setId {setId}"}