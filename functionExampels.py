from Helper import Helper

# s = getActiveSeason(False)

# eId = getEventIdFromName(s, "monte-carlo")
# print(eId)

# itinerary = getItinerary(eId)
# # print([{"itineraryLegId": i['itineraryLegId'], "itineraryId": i["itineraryId"], "startListId": i["startListId"], "name": i["name"], "legDate": i["name"], "order": i["order"], "status": i["status"]} for i in itinerary])

# sections = getSections(itinerary)
# # print(sections)

# # controls = getControls(sections)

# stages = getStages(sections)
# # print(stages)

# # stageList = getStageList(stages)
# # # print(stageList)

# # stagesLookup = getStagesLookup(stages)
# # print(stagesLookup)

# stageId = getStageId(stages, "Col de Turini 1", "name")
# # print(stageId)

# # stageInfo = getStageInfo(stages, stageId)
# # # print(stageInfo)

# # # startListId = next((item["startListId"] for item in itinerary if "friday" in item['name'].lower()), None)
# # startListId = getStartListId(itinerary, stages[0]['itinerarySectionId'])
# # # print(startListId)

# # startList = getStartList(eId, startListId)
# # # print(startList)

# # entries = getRallyEntries(eId)
# # # print(entries)

# # wrcEntries = [e['entryId'] for e in entries if e['group']['name'] == 'Rally1']
# # # print(wrcEntries)

# # drivers = getDrivers(entries)
# # # print(drivers)

# # codrivers = getCoDrivers(entries)
# # # print(codrivers)

# # ogierDriverId = getPersonId(drivers, 'ogier')
# # # print(ogierDriverId)

# # ogierEntryId = next((entry['entryId'] for entry in entries if entry['driverId'] == ogierDriverId), None)
# # # print(ogierEntryId)

# # print(getCarData(entries)[:2])

# # print(getPenalties(eId))

# # print(getRetirements(eId))

# # print(getResult(eId))

# # print(getStageWinners(eId))

# # overallResult = getOverallResult(eId, stageId)
# # print(overallResult[:2])

# # stageList = [4161, 4162]
# # multiOverallResult = getMultipleOverall(eId, stageList)
# # print(multiOverallResult[len(multiOverallResult)-2:len(multiOverallResult)])

# # stageTimes = getStageTimes(eId, stageId)
# # print(stageTimes[:2])

# # stageList = [4161, 4162]
# # multiStageTimes = getMultipleStageTimes(eId, stageList)
# # print(multiStageTimes[:2])

# # multiStageTimesWide = getMultiStageTimesWide(multiStageTimes)
# # print(multiStageTimesWide[:2])

# # multiStagePositionsWide = getMultiStageGenericWide(multiStageTimes, 'position')
# # print(multiStagePositionsWide[:2])

# # splits = getSplits(eId, stageId)
# # print(splits['splitPoints'])

# # driverSplits = getDriverSplits(splits)
# # print(driverSplits[:2])

# # driverSplitsWide = getDriverSplitsWide(splits)
# # print(driverSplitsWide[:2])

# stageList = [4161, 4162]
# multiSplitTimes = getMultiSplitTimes(eId, stageList)
# print(multiSplitTimes[:3])