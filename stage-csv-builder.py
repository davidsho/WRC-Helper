import pandas as pd
from Helper import Helper

helper = Helper()
s = helper.getActiveSeason()
eventIds = helper.getEventIds(s)

for eId in eventIds:
    itinerary = helper.getItinerary(eId)
    sections = helper.getSections(itinerary)
    stages = helper.getStages(sections)
    stages = helper.getStageList(stages)

    multiStageTimes = helper.getMultipleStageTimes(eId, stages)
    multiStagePositions = helper.getMultiStageGenericWide(multiStageTimes, 'position')
    df = pd.DataFrame(multiStagePositions)
    df.to_csv("./events/"+str(eId)+"-stage-positions.csv")