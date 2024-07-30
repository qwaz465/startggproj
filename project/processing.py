from the_project import *
from queries import *
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
def playerList(sets):
    players = set()
    print(type(players))
    print(players)
    for smashSet in sets:
        print(smashSet)
        names = list(smashSet.keys())
        print(names)
        p1name = names[0]
        p2name = names[1]
        players.add(p1name)
        players.add(p2name)
    return players