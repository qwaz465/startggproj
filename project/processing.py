from the_project import *
from queries import *
# for 1 tournament, grab all sets by page and adds IDs to setList and returns it
def getSetIDs(eventID):
    setList = []
    # getting page count for bracket
    totalPages = getTotalPagesSet(eventID)
    for page in range(1, totalPages + 1):
        # getting all set maps on a page
        sets = getSetsOnePage(eventID, page)
        # getting actual set IDs
        for setMap in sets:
            set = setMap['id']
            setList.append(set)
    return setList