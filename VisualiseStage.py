import pandas as pd
from Helper import Helper

helper = Helper()
s = helper.getActiveSeason()
eventId = helper.getEventIdFromName(s, "monte-carlo")
helper.getItinerary(eventId)
result = pd.DataFrame(helper.getStageWinners(eventId))
print(result)

entries = helper.getRallyEntries(eventId)
winners = pd.DataFrame([helper.getCarDataFromEntry(helper.getEntryById(entries, winner)) for winner in result['entryId']])
print(winners.columns)
