import pandas as pd
from Helper import Helper

helper = Helper()
s = helper.getActiveSeason()
eventIds = helper.getEventIds(s)

for eId in eventIds:
    entries = helper.getRallyEntries(eId)
    cars = helper.getCarData(entries)

    data = pd.DataFrame(entries)
    data.to_csv("./entries/"+str(eId)+"-entries.csv")
